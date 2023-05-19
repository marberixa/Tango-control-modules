from PyTango import DeviceProxy
from sardana import State, DataAccess
from sardana.pool.controller import DefaultValue, MotorController
from sardana.pool.controller import Type, Access, Description

class StandaMotorController(MotorController):
    
    axis_attributes = {
        'Tango_Device': {
            Type: str,
            Description: 'The Tango Device'\
                ' (e.g. domain/family/member)',
            Access: DataAccess.ReadWrite,
            DefaultValue: "a/b/c"
        },
    }
    
    def __init__(self, inst, props, *args, **kwargs): #инициализация устройства
        super(StandaMotorController, self).__init__(inst, props, *args, **kwargs)
        self.axis_extra_pars = {}

    def AddDevice(self, axis):      #добавление устройства
        self.axis_extra_pars[axis] = {}

    def DeleteDevice(self, axis):       #удаление устройства
        del self.axis_extra_pars[axis]

    def StateOne(self, axis):   #статус движения
        #state = self.axis_extra_pars[axis]['Proxy'].command_inout("State")
        #status = self.axis_extra_pars[axis]['Proxy'].command_inout("Status")
        if (self.axis_extra_pars[axis]['Proxy'].read_attribute("curSpeed").value != 0): 
           return State.Moving
        else: return State.On
        #return state

    def ReadOne(self, axis):
        ret = self.axis_extra_pars[axis]['Proxy'].read_attribute("curPosition").value #тек. положение
        return ret
        
    def StartOne(self, axis, position):
        self.axis_extra_pars[axis]['Proxy'].command_inout("Move", position)  #перемещение в заданное положение

    def StopOne(self, axis):
        self.axis_extra_pars[axis]['Proxy'].command_inout("Sstop")      #плавная остановка             

    def AbortOne(self, axis):
        self.axis_extra_pars[axis]['Proxy'].command_inout("Stop")       #немедленная остановка                   


    def SetAxisPar(self, axis, name, value):        #установка хар-к движения
        if self.axis_extra_pars[axis]['Proxy']:
            if name == 'velocity':
                self.axis_extra_pars[axis]['Proxy'].write_attribute("speed", value)
            elif name == 'acceleration':
                self.axis_extra_pars[axis]['Proxy'].write_attribute("accel", value)
            elif name == 'deceleration':
                self.axis_extra_pars[axis]['Proxy'].write_attribute("decel", value)
            else:
                self._log.debug('Parameter %s is not set' % name)

    def GetAxisPar(self, axis, name):   #чтение хар-к движения
        if self.axis_extra_pars[axis]['Proxy']:
            if name == 'velocity':
                result = self.axis_extra_pars[axis]['Proxy'].read_attribute("speed").value
            elif name == 'acceleration':
                result = self.axis_extra_pars[axis]['Proxy'].read_attribute("accel").value
            elif name == 'deceleration':
                result = self.axis_extra_pars[axis]['Proxy'].read_attribute("decel").value
            else:
                result = None
        else:
            result = None
        return result

    def GetAxisExtraPar(self, axis, name):
        return self.axis_extra_pars[axis][name]
    
    def SetAxisExtraPar(self, axis, name, value):       #связь с Tango DeviceServer
        if name == 'Tango_Device':
            self.axis_extra_pars[axis][name] = value
            try:
                self.axis_extra_pars[axis]['Proxy'] = DeviceProxy(value)
                self._log.info('axis {:d} DeviceProxy set to: {:s}'.format(axis, value))
            except Exception as e:
                self.axis_extra_pars[axis]['Proxy'] = None
                raise e