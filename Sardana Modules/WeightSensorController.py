from PyTango import DeviceProxy

from sardana import State
from sardana.pool.controller import CounterTimerController
from sardana.pool.controller import ZeroDController

from sardana import DataAccess
from sardana.pool.controller import Type, Description, DefaultValue, Access, FGet, FSet


class WeightSensorController(ZeroDController):

    axis_attributes = {
        'Tango_Device': {
            Type: str,
            Description: 'The Tango Device'\
                ' (e.g. domain/family/member)',
            Access: DataAccess.ReadWrite,
            DefaultValue: "a/b/c"
        },
    }

    def __init__(self, inst, props, *args, **kwargs):
        super(WeightSensorController, self).__init__(inst, props, *args, **kwargs)
        # initialize hardware communication
        # do some initialization
        self._counters = {}

    def AddDevice(self, axis):
        self._counters[axis] = {}

    def DeleteDevice(self, axis):
        del self._counters[axis]

    def StateOne(self, axis):
        state = self._counters[axis]['Proxy'].command_inout("State")
        status = self._counters[axis]['Proxy'].command_inout("Status")
        return state, status

    def ReadOne(self, axis):
        value = self._counters[axis]['Proxy'].read_attribute("weight").value
        return value
        #передача значения для наглядности
        #value = DeviceProxy("sys/tg_test/1").read_attribute("weight").value

    def StartOne(self, axis, position=None):
        pass

    def StopOne(self, axis):
        pass

    def AbortOne(self, axis):
        pass

    
    def GetAxisExtraPar(self, axis, name):
        return self._counters[axis][name]
    
    def SetAxisExtraPar(self, axis, name, value):
        if name == 'Tango_Device':
            self._counters[axis][name] = value
            try:
                self._counters[axis]['Proxy'] = DeviceProxy(value)
                self._log.info('axis {:d} DeviceProxy set to: {:s}'.format(axis, value))
            except Exception as e:
                self._counters[axis]['Proxy'] = None
                raise e