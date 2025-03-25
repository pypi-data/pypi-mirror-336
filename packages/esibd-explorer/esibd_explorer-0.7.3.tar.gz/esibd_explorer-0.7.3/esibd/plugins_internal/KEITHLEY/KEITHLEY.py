# pylint: disable=[missing-module-docstring] # see class docstrings
import time
from threading import Thread
import numpy as np
from PyQt6.QtCore import pyqtSignal
import pyvisa
from esibd.plugins import Device
from esibd.core import Parameter, parameterDict, PluginManager, Channel, PRINT, DeviceController, getTestMode

def providePlugins():
    return [KEITHLEY]

class KEITHLEY(Device):
    """Device that contains a list of current channels, each corresponding to a single KEITHLEY 6487 picoammeter."""
    documentation = None # use __doc__

    name = 'KEITHLEY'
    version = '1.0'
    supportedVersion = '0.7'
    pluginType = PluginManager.TYPE.OUTPUTDEVICE
    unit = 'pA'
    iconFile = 'keithley.png'

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.useOnOffLogic = True
        self.channelType = CurrentChannel
        self.useBackgrounds = True # record backgrounds for data correction

    def initGUI(self):
        super().initGUI()
        self.addAction(event=lambda: self.resetCharge(), toolTip=f'Reset accumulated charge for {self.name}.', icon='battery-empty.png')

    def getDefaultSettings(self):
        """ Define device specific settings that will be added to the general settings tab.
        These will be included if the settings file is deleted and automatically regenerated.
        Overwrite as needed."""
        defaultSettings = super().getDefaultSettings()
        defaultSettings[f'{self.name}/Interval'][Parameter.VALUE] = 100 # overwrite default value
        return defaultSettings

    def getInitializedChannels(self):
        return [channel for channel in self.channels if (channel.enabled and (channel.controller.port is not None or self.getTestMode())) or not channel.active]

    def resetCharge(self):
        for channel in self.channels:
            channel.resetCharge()

    def closeCommunication(self):
        self.setOn(False)
        for channel in self.channels:
            channel.controller.voltageON(parallel=False)
        super().closeCommunication()

    def setOn(self, on=None):
        super().setOn(on)
        if self.initialized():
            for channel in self.channels:
                channel.controller.voltageON()
        elif self.isOn():
            self.initializeCommunication()

    def updateTheme(self):
        """:meta private:"""
        super().updateTheme()
        self.onAction.iconTrue = self.getIcon()
        self.onAction.updateIcon(self.isOn())

class CurrentChannel(Channel):
    """UI for picoammeter with integrated functionality"""

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.controller = CurrentController(_parent=self)
        self.preciseCharge = 0 # store independent of spin box precision to avoid rounding errors

    CHARGE     = 'Charge'
    ADDRESS    = 'Address'
    VOLTAGE    = 'Voltage'

    def getDefaultChannel(self):
        channel = super().getDefaultChannel()
        channel[self.VALUE][Parameter.HEADER ] = 'I (pA)' # overwrite existing parameter to change header
        channel[self.CHARGE     ] = parameterDict(value=0, widgetType=Parameter.TYPE.FLOAT, advanced=False, header='C (pAh)', indicator=True, attr='charge')
        channel[self.ADDRESS    ] = parameterDict(value='GPIB0::22::INSTR', widgetType=Parameter.TYPE.TEXT, advanced=True, attr='address')
        channel[self.VOLTAGE    ] = parameterDict(value=0, widgetType=Parameter.TYPE.FLOAT, advanced=False, attr='voltage', event=lambda: self.controller.applyVoltage())
        return channel

    def setDisplayedParameters(self):
        super().setDisplayedParameters()
        self.insertDisplayedParameter(self.CHARGE, before=self.DISPLAY)
        self.insertDisplayedParameter(self.VOLTAGE, before=self.DISPLAY)
        self.displayedParameters.append(self.ADDRESS)

    def tempParameters(self):
        return super().tempParameters() + [self.CHARGE]

    def enabledChanged(self):
        super().enabledChanged()
        if self.device.liveDisplayActive() and self.device.recording:
            if self.enabled:
                self.controller.initializeCommunication()
            elif self.controller.acquiring:
                self.controller.stopAcquisition()

    def appendValue(self, lenT, nan=False):
        super().appendValue(lenT, nan=nan)
        if not nan and not np.isnan(self.value) and not np.isinf(self.value):
            chargeIncrement = (self.value-self.background)*self.device.interval/1000/3600 if self.values.size > 1 else 0
            self.preciseCharge += chargeIncrement # display accumulated charge # don't use np.sum(self.charges) to allow
            self.charge = self.preciseCharge # pylint: disable=[attribute-defined-outside-init] # attribute defined dynamically

    def clearHistory(self, max_size=None):
        super().clearHistory(max_size)
        self.resetCharge()

    def resetCharge(self):
        self.charge = 0 # pylint: disable=[attribute-defined-outside-init] # attribute defined dynamically
        self.preciseCharge = 0

    def realChanged(self):
        self.getParameterByName(self.ADDRESS).getWidget().setVisible(self.real)
        super().realChanged()

class CurrentController(DeviceController):
    """Implements visa communication with KEITHLEY 6487."""

    class SignalCommunicate(DeviceController.SignalCommunicate):
        updateValueSignal = pyqtSignal(float)

    def __init__(self, _parent):
        super().__init__(_parent=_parent)
        #setup port
        self.channel = _parent
        self.device = self.channel.getDevice()
        self.port = None
        self.phase = np.random.rand()*10 # used in test mode
        self.omega = np.random.rand() # used in test mode
        self.offset = np.random.rand()*10 # used in test mode

    def initializeCommunication(self):
        if self.channel.enabled and self.channel.active and self.channel.real:
            super().initializeCommunication()
        else:
            self.stopAcquisition()

    def closeCommunication(self):
        if self.port is not None:
            with self.lock.acquire_timeout(1, timeoutMessage='Could not acquire lock before closing port.'):
                self.port.close()
                self.port = None
        super().closeCommunication()

    def runInitialization(self):
        try:
            # name = rm.list_resources()
            self.rm = pyvisa.ResourceManager()
            self.port = self.rm.open_resource(self.channel.address)
            self.port.write("*RST")
            self.device.print(self.port.query('*IDN?'))
            self.port.write("SYST:ZCH OFF")
            self.port.write("CURR:NPLC 6")
            self.port.write("SOUR:VOLT:RANG 50")
            self.signalComm.initCompleteSignal.emit()
        except Exception:
            self.signalComm.updateValueSignal.emit(np.nan)
        finally:
            self.initializing = False

    def initComplete(self):
        super().initComplete()
        self.voltageON()

    def startAcquisition(self):
        if self.channel.active:
            super().startAcquisition()

    def runAcquisition(self, acquiring):
        while acquiring():
            with self.lock.acquire_timeout(1) as lock_acquired:
                if lock_acquired:
                    if getTestMode():
                        self.fakeNumbers()
                    else:
                        self.readNumbers()
                        # no sleep needed, timing controlled by waiting during readNumbers
            if getTestMode():
                time.sleep(self.channel.device.interval/1000)

    def updateValue(self, value):
        self.channel.value = value

    def applyVoltage(self):
        if self.port is not None:
            self.port.write(f"SOUR:VOLT {self.channel.voltage}")

    def voltageON(self, parallel=True): # this can run in main thread
        if not getTestMode() and self.initialized:
            self.applyVoltage() # apply voltages before turning power supply on or off
            if parallel:
                Thread(target=self.voltageONFromThread, name=f'{self.device.name} voltageONFromThreadThread').start()
            else:
                self.voltageONFromThread()

    def voltageONFromThread(self):
        self.port.write(f"SOUR:VOLT:STAT {'ON' if self.device.isOn() else 'OFF'}")

    def fakeNumbers(self):
        if not self.channel.device.pluginManager.closing:
            if self.channel.enabled and self.channel.active and self.channel.real:
                self.signalComm.updateValueSignal.emit(np.sin(self.omega*time.time()/5+self.phase)*10+np.random.rand()+self.offset)

    def readNumbers(self):
        if not self.channel.device.pluginManager.closing:
            if self.channel.enabled and self.channel.active and self.channel.real:
                try:
                    self.port.write("INIT")
                    self.signalComm.updateValueSignal.emit(float(self.port.query("FETCh?").split(',')[0][:-1])*1E12)
                except (pyvisa.errors.VisaIOError, pyvisa.errors.InvalidSession, AttributeError) as e:
                    self.print(f'Error while reading current {e}', flag=PRINT.ERROR)
                    self.errorCount += 1
                    self.signalComm.updateValueSignal.emit(np.nan)
