# pylint: disable=[missing-module-docstring] # see class docstrings
import time
import h5py
import serial
import numpy as np
from PyQt6.QtCore import pyqtSignal
from esibd.plugins import Device, StaticDisplay, Scan
from esibd.core import Parameter, parameterDict, PluginManager, Channel, PRINT, DeviceController, MetaChannel, getTestMode

def providePlugins():
    return [RBD]

class RBD(Device):
    """Device that contains a list of current channels, each corresponding to a single RBD
    9103 picoammeter. The channels show the accumulated charge over time,
    which is proportional to the number of deposited ions. It can also
    reveal on which elements ions are lost."""
    documentation = None # use __doc__

    name = 'RBD'
    version = '1.0'
    supportedVersion = '0.7'
    pluginType = PluginManager.TYPE.OUTPUTDEVICE
    unit = 'pA'
    iconFile = 'RBD.png'

    class StaticDisplay(StaticDisplay):
        """A display for device data from files."""

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.previewFileTypes.append('.cur.rec')
            self.previewFileTypes.append('.cur.h5')
            self.previewFileTypes.append('OUT.h5')

        def loadDataInternal(self, file):
            """Extending to support legacy files"""
            if file.name.endswith('.cur.rec'):  # legacy ESIBD Control file
                with open(file, 'r', encoding=self.UTF8) as dataFile:
                    dataFile.readline()
                    headers = dataFile.readline().split(',') # read names from second line
                try:
                    data = np.loadtxt(file, skiprows=4, delimiter=',', unpack=True)
                except ValueError as e:
                    self.print(f'Loading from {file.name} failed: {e}', PRINT.ERROR)
                    return
                if data.shape[0] == 0:
                    self.print(f'No data found in file {file.name}.', PRINT.ERROR)
                    return
                for dat, header in zip(data, headers):
                    self.outputs.append(MetaChannel(parentPlugin=self, name=header.strip(), recordingData=np.array(dat), recordingBackground=np.zeros(dat.shape[0]), unit='pA'))
                if len(self.outputs) > 0: # might be empty
                    # need to fake time axis as it was not implemented
                    self.inputs.append(MetaChannel(parentPlugin=self, name=self.TIME, recordingData=np.linspace(0, 120000, self.outputs[0].getRecordingData().shape[0])))
            elif file.name.endswith('.cur.h5'):
                with h5py.File(file, 'r') as h5file:
                    self.inputs.append(MetaChannel(parentPlugin=self, name=self.TIME, recordingData=h5file[self.TIME][:]))
                    output_group = h5file['Current']
                    for name, item in output_group.items():
                        if '_BG' in name:
                            self.outputs[-1].recordingBackground = item[:]
                        else:
                            self.outputs.append(MetaChannel(parentPlugin=self, name=name, recordingData=item[:], unit='pA'))
            elif file.name.endswith('OUT.h5'): # old Output format when EBD was the only output
                with h5py.File(file, 'r') as h5file:
                    self.inputs.append(MetaChannel(parentPlugin=self, name=self.TIME, recordingData=h5file[Scan.INPUTCHANNELS][self.TIME][:]))
                    output_group = h5file[Scan.OUTPUTCHANNELS]
                    for name, item in output_group.items():
                        if '_BG' in name:
                            self.outputs[-1].recordingBackground = item[:]
                        else:
                            self.outputs.append(MetaChannel(parentPlugin=self, name=name, recordingData=item[:], unit=item.attrs[Scan.UNIT] if Scan.UNIT in item.attrs else ''))
            else:
                return super().loadDataInternal(file)
            return True

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
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

class CurrentChannel(Channel):
    """UI for picoammeter with integrated functionality"""

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.controller = CurrentController(_parent=self)
        self.preciseCharge = 0 # store independent of spin box precision to avoid rounding errors

    CHARGE     = 'Charge'
    COM        = 'COM'
    DEVICENAME = 'Devicename'
    RANGE      = 'Range'
    AVERAGE    = 'Average'
    BIAS       = 'Bias'
    OUTOFRANGE = 'OutOfRange'
    UNSTABLE   = 'Unstable'
    ERROR      = 'Error'

    def getDefaultChannel(self):
        channel = super().getDefaultChannel()
        channel[self.VALUE][Parameter.HEADER ] = 'I (pA)' # overwrite existing parameter to change header
        channel[self.CHARGE     ] = parameterDict(value=0, widgetType=Parameter.TYPE.FLOAT, advanced=False, header='C (pAh)', indicator=True, attr='charge')
        channel[self.COM        ] = parameterDict(value='COM1', widgetType=Parameter.TYPE.COMBO, advanced=True, toolTip='COM port',
                                        items=','.join([f'COM{x}' for x in range(1, 25)]), header='COM', attr='com')
        channel[self.DEVICENAME ] = parameterDict(value='smurf', widgetType=Parameter.TYPE.LABEL, advanced=True, attr='devicename')
        channel[self.RANGE      ] = parameterDict(value='auto', widgetType=Parameter.TYPE.COMBO, advanced=True,
                                        items='auto, 2 nA, 20 nA, 200 nA, 2 µA, 20 µA, 200 µA, 2 mA', attr='range',
                                        event=lambda: self.updateRange(), toolTip='Sample range. Defines resolution.')
        channel[self.AVERAGE    ] = parameterDict(value='off', widgetType=Parameter.TYPE.COMBO, advanced=True,
                                        items='off, 2, 4, 8, 16, 32', attr='average',
                                        event=lambda: self.updateAverage(), toolTip='Running average on hardware side.')
        channel[self.BIAS       ] = parameterDict(value=False, widgetType=Parameter.TYPE.BOOL, advanced=True,
                                        toolTip='Apply internal bias.', attr='bias', event=lambda: self.updateBias())
        channel[self.OUTOFRANGE ] = parameterDict(value=False, widgetType=Parameter.TYPE.BOOL, advanced=False, indicator=True,
                                        header='OoR', toolTip='Indicates if signal is out of range.', attr='outOfRange')
        channel[self.UNSTABLE   ] = parameterDict(value=False, widgetType=Parameter.TYPE.BOOL, advanced=False, indicator=True,
                                        header='U', toolTip='Indicates if signal is out of unstable.', attr='unstable')
        channel[self.ERROR      ] = parameterDict(value='', widgetType=Parameter.TYPE.LABEL, advanced=False, attr='error', indicator=True)
        return channel

    def setDisplayedParameters(self):
        super().setDisplayedParameters()
        self.insertDisplayedParameter(self.CHARGE, before=self.DISPLAY)
        self.displayedParameters.append(self.COM)
        self.displayedParameters.append(self.DEVICENAME)
        self.displayedParameters.append(self.RANGE)
        self.displayedParameters.append(self.AVERAGE)
        self.displayedParameters.append(self.BIAS)
        self.displayedParameters.append(self.OUTOFRANGE)
        self.displayedParameters.append(self.UNSTABLE)
        self.displayedParameters.append(self.ERROR)

    def tempParameters(self):
        return super().tempParameters() + [self.CHARGE, self.OUTOFRANGE, self.UNSTABLE, self.ERROR]

    def enabledChanged(self):
        super().enabledChanged()
        if self.controller.initialized:
            if self.enabled:
                self.controller.initializeCommunication()
            elif self.controller.acquiring:
                self.controller.stopAcquisition()

    def appendValue(self, lenT, nan=False):
        # calculate deposited charge in last time step for all channels
        # this does not only measure the deposition current but also on what lenses current is lost
        # make sure that the data interval is the same as used in data acquisition
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
        self.getParameterByName(self.COM).getWidget().setVisible(self.real)
        self.getParameterByName(self.DEVICENAME).getWidget().setVisible(self.real)
        self.getParameterByName(self.RANGE).getWidget().setVisible(self.real)
        self.getParameterByName(self.AVERAGE).getWidget().setVisible(self.real)
        self.getParameterByName(self.BIAS).getWidget().setVisible(self.real)
        self.getParameterByName(self.OUTOFRANGE).getWidget().setVisible(self.real)
        self.getParameterByName(self.UNSTABLE).getWidget().setVisible(self.real)
        if self.device.recording:
            self.controller.initializeCommunication()
        super().realChanged()

    def activeChanged(self):
        if self.device.recording:
            self.controller.initializeCommunication()
        return super().activeChanged()

    def updateAverage(self):
        if self.controller is not None and self.controller.acquiring:
            self.controller.updateAverageFlag = True

    def updateRange(self):
        if self.controller is not None and self.controller.acquiring:
            self.controller.updateRangeFlag = True

    def updateBias(self):
        if self.controller is not None and self.controller.acquiring:
            self.controller.updateBiasFlag = True

class CurrentController(DeviceController):

    class SignalCommunicate(DeviceController.SignalCommunicate):
        updateValueSignal = pyqtSignal(float, bool, bool, str)
        updateDeviceNameSignal = pyqtSignal(str)

    def __init__(self, _parent):
        super().__init__(_parent=_parent)
        #setup port
        self.channel = _parent
        self.device = self.channel.getDevice()
        self.port = None
        self.signalComm.updateDeviceNameSignal.connect(self.updateDeviceName)
        self.updateAverageFlag = False
        self.updateRangeFlag = False
        self.updateBiasFlag = False
        self.phase = np.random.rand()*10 # used in test mode
        self.omega = np.random.rand() # used in test mode
        self.offset = np.random.rand()*10 # used in test mode

    def initializeCommunication(self):
        if self.channel.enabled and self.channel.active and self.channel.real:
            super().initializeCommunication()
        else:
            self.stopAcquisition() # as this is a channel controller it should only stop acquisition but not recording

    def closeCommunication(self):
        if self.port is not None:
            with self.lock.acquire_timeout(1, timeoutMessage=f'Could not acquire lock before closing port of {self.channel.devicename}.') as lock_acquired:
                if self.initialized and lock_acquired:  # pylint: disable=[access-member-before-definition] # defined in DeviceController class
                    self.RBDWriteRead('I0000', lock_acquired=lock_acquired) # stop sampling
                self.port.close()
                self.port = None
        super().closeCommunication()

    def runInitialization(self):
        try:
            self.port=serial.Serial(
                f'{self.channel.com}',
                baudrate=57600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                xonxoff=False,
                timeout=3)
            self.setRange()
            self.setAverage()
            self.setGrounding()
            self.setBias()
            name = self.getName()
            if name == '':
                self.signalComm.updateValueSignal.emit(0, False, False, f'Device at port {self.channel.com} did not provide a name. Abort initialization.')
                return
            self.signalComm.updateValueSignal.emit(0, False, False, f'{name} initialized at {self.channel.com}')
            self.signalComm.updateDeviceNameSignal.emit(name) # pass port to main thread as init thread will die
            self.signalComm.initCompleteSignal.emit()
        except serial.serialutil.PortNotOpenError as e:
            self.signalComm.updateValueSignal.emit(0, False, False, f'Port {self.channel.com} is not open: {e}')
        except serial.serialutil.SerialException as e:
            self.signalComm.updateValueSignal.emit(0, False, False, f'9103 not found at {self.channel.com}: {e}')
        finally:
            self.initializing = False

    def startAcquisition(self):
        if self.channel.active and self.channel.real:
            super().startAcquisition()

    def runAcquisition(self, acquiring):
        if not getTestMode():
            self.RBDWriteRead(message=f'I{self.channel.getDevice().interval:04d}') # start sampling with given interval (implement high speed communication if available)
        while acquiring():
            with self.lock.acquire_timeout(1, timeoutMessage=f'Cannot acquire lock to read current from {self.channel.devicename}.') as lock_acquired:
                if lock_acquired:
                    if getTestMode():
                        self.fakeNumbers()
                    else:
                        self.readNumbers() # no sleep needed, timing controlled by waiting during readNumbers
                    self.updateParameters()
            if getTestMode():
                time.sleep(self.channel.getDevice().interval/1000)

    def updateDeviceName(self, name):
        self.channel.devicename = name

    def updateValue(self, value, outOfRange, unstable, error=''): # # pylint: disable=[arguments-differ] # arguments differ by intention
        self.channel.value = value
        self.channel.outOfRange = outOfRange
        self.channel.unstable = unstable
        self.channel.error = error
        if error != '' and self.channel.getDevice().log:
            self.print(error)

    def setRange(self):
        self.RBDWriteRead(message=f'R{self.channel.getParameterByName(self.channel.RANGE).getWidget().currentIndex()}') # set range
        self.updateRangeFlag=False

    def setAverage(self):
        _filter = self.channel.getParameterByName(self.channel.AVERAGE).getWidget().currentIndex()
        _filter = 2**_filter if _filter > 0 else 0
        self.RBDWriteRead(message=f'F0{_filter:02}') # set filter
        self.updateAverageFlag=False

    def setBias(self):
        self.RBDWriteRead(message=f'B{int(self.channel.bias)}') # set bias, convert from bool to int
        self.updateBiasFlag=False

    def setGrounding(self):
        self.RBDWriteRead(message='G0') # input grounding off

    def getName(self):
        if not getTestMode():
            name = self.RBDWriteRead(message='P') # get channel name
        else:
            name = 'UNREALSMURF'
        if '=' in name:
            return name.split('=')[1]
        else:
            return ''

    def updateParameters(self):
        # call from runAcquisition to make sure there are no race conditions
        if self.updateRangeFlag:
            self.setRange()
        if self.updateAverageFlag:
            self.setAverage()
        if self.updateBiasFlag:
            self.setBias()

    def command_identify(self):
        with self.lock:
            self.RBDWrite('Q') # put in autorange
            for _ in range(13):
                message = self.RBDRead()
                self.print(message)
            #if 'PID' in message:
           #     return message.split('=')[1] # return channel name
       # return 'channel name not found'
        # self.print(message, message.split('='))
        # self.print(self.RBDRead()) # -> b'RBD Instruments: PicoAmmeter\r\n'
        # self.print(self.RBDRead()) # -> b'Firmware Version: 02.09\r\n'
        # self.print(self.RBDRead()) # -> b'Build: 1-25-18\r\n'
        # self.print(self.RBDRead()) # -> b'R, Range=AutoR\r\n'
        # self.print(self.RBDRead()) # -> b'I, sample Interval=0000 mSec\r\n'
        # self.print(self.RBDRead()) # -> b'L, Chart Log Update Interval=0200 mSec\r\n'
        # self.print(self.RBDRead()) # -> b'F, Filter=032\r\n'
        # self.print(self.RBDRead()) # -> b'B, BIAS=OFF\r\n'
        # self.print(self.RBDRead()) # -> b'V, FormatLen=5\r\n'
        # self.print(self.RBDRead()) # -> b'G, AutoGrounding=DISABLED\r\n'
        # self.print(self.RBDRead()) # -> b'Q, State=MEASURE\r\n'
        # self.print(self.RBDRead()) # -> b'P, PID=TRACKSMURF\r\n'
        # self.print(self.RBDRead()) # -> b'P, PID=TRACKSMURF\r\n'

    def fakeNumbers(self):
        if not self.channel.getDevice().pluginManager.closing:
            if self.channel.enabled and self.channel.active and self.channel.real:
                self.signalComm.updateValueSignal.emit(np.sin(self.omega*time.time()/5+self.phase)*10+np.random.rand()+self.offset, False, False, '')

    def readNumbers(self):
        if not self.channel.getDevice().pluginManager.closing:
            if self.channel.enabled and self.channel.active and self.channel.real:
                msg = ''
                msg=self.RBDRead()
                if not self.acquiring: # may have changed while waiting on message
                    return
                parsed = self.parse_message_for_sample(msg)
                if any (sym in parsed for sym in ['<','>']):
                    self.signalComm.updateValueSignal.emit(0, True, False, parsed)
                elif '*' in parsed:
                    self.signalComm.updateValueSignal.emit(0, False, True, parsed)
                elif parsed == '':
                    self.signalComm.updateValueSignal.emit(0, False, False, 'got empty message')
                else:
                    self.signalComm.updateValueSignal.emit(self.readingToNum(parsed), False, False, '')

    #Single sample (standard speed) message parsing
    def parse_message_for_sample(self, msg):
        if '&S' in msg:
            return msg.strip('&')
        else:
            return ''

    def readingToNum(self, parsed):  # convert to pA
        """Converts string to float value of pA based on unit"""
        try:
            _, _, x, unit = parsed.split(',')
            x=float(x)
        except ValueError as e:
            self.print(f'Error while parsing current; {parsed}, Error: {e}', PRINT.ERROR)
            self.errorCount += 1
            return self.channel.value # keep last valid value
        match unit:
            case 'mA':
                return x*1E9
            case 'uA':
                return x*1E6
            case 'nA':
                return x*1E3
            case 'pA':
                return x*1
            case _:
                self.print(f'Error: No handler for unit {unit} implemented!', PRINT.ERROR)
                return self.channel.value # keep last valid value
                #raise ValueError(f'No handler for unit {u} implemented!')

    def RBDWrite(self, message):
        self.serialWrite(self.port, f'&{message}\n')

    def RBDRead(self):
        return self.serialRead(self.port)

    def RBDWriteRead(self, message, lock_acquired=False):
        response = ''
        if not getTestMode():
            with self.lock.acquire_timeout(1, timeoutMessage=f'Cannot acquire lock for message: {message}.', lock_acquired=lock_acquired) as lock_acquired:
                if lock_acquired:
                    self.RBDWrite(message) # get channel name
                    response = self.RBDRead()
        return response
