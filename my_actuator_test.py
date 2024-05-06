
import os
import can
import myactuator_rmd_py as rmd



if __name__ == "__main__":
    #Set CAN0 speed to 1M bps
    os.system('sudo ifconfig can0 down')
    os.system('sudo ip link set can0 type can bitrate 1000000')
    os.system("sudo ifconfig can0 txqueuelen 100000")
    os.system('sudo ifconfig can0 up')

    driver = rmd.CanDriver("can0")
    m = rmd.ActuatorInterface(driver, 1)
    m.getVersionDate()



    

    # actuator.sendPositionAbsoluteSetpoint(0, 500.0)
    # actuator.shutdownMotor()


"""
class ActuatorInterface(pybind11_builtins.pybind11_object)
 |  Method resolution order:
 |      ActuatorInterface
 |      pybind11_builtins.pybind11_object
 |      builtins.object
 |  
 |  Methods defined here:
 |  
 |  __init__(...)
 |      __init__(self: myactuator_rmd_py.ActuatorInterface, arg0: myactuator_rmd_py.Driver, arg1: int) -> None
 |  
 |  getAcceleration(...)
 |      getAcceleration(self: myactuator_rmd_py.ActuatorInterface) -> int
 |  
 |  getCanId(...)
 |      getCanId(self: myactuator_rmd_py.ActuatorInterface) -> int
 |  
 |  getControlMode(...)
 |      getControlMode(self: myactuator_rmd_py.ActuatorInterface) -> myactuator_rmd::ControlMode
 |  
 |  getControllerGains(...)
 |      getControllerGains(self: myactuator_rmd_py.ActuatorInterface) -> myactuator_rmd::Gains
 |  
 |  getMotorModel(...)
 |      getMotorModel(self: myactuator_rmd_py.ActuatorInterface) -> str
 |  
 |  getMotorPower(...)
 |      getMotorPower(self: myactuator_rmd_py.ActuatorInterface) -> float
 |  
 |  getMotorStatus1(...)
 |      getMotorStatus1(self: myactuator_rmd_py.ActuatorInterface) -> myactuator_rmd::MotorStatus1
|  getMotorStatus2(...)
 |      getMotorStatus2(self: myactuator_rmd_py.ActuatorInterface) -> myactuator_rmd::MotorStatus2
 |  
 |  getMotorStatus3(...)
 |      getMotorStatus3(self: myactuator_rmd_py.ActuatorInterface) -> myactuator_rmd::MotorStatus3
 |  
 |  getMultiTurnAngle(...)
 |      getMultiTurnAngle(self: myactuator_rmd_py.ActuatorInterface) -> float
 |  
 |  getMultiTurnEncoderOriginalPosition(...)
 |      getMultiTurnEncoderOriginalPosition(self: myactuator_rmd_py.ActuatorInterface) -> int
 |  
 |  getMultiTurnEncoderPosition(...)
 |      getMultiTurnEncoderPosition(self: myactuator_rmd_py.ActuatorInterface) -> int
 |  
 |  getMultiTurnEncoderZeroOffset(...)
 |      getMultiTurnEncoderZeroOffset(self: myactuator_rmd_py.ActuatorInterface) -> int
 |  
 |  getRuntime(...)
 |      getRuntime(self: myactuator_rmd_py.ActuatorInterface) -> datetime.timedelta
 |  
 |  getSingleTurnAngle(...)
 |      getSingleTurnAngle(self: myactuator_rmd_py.ActuatorInterface) -> float
 |  
 |  getSingleTurnEncoderPosition(...)
 |      getSingleTurnEncoderPosition(self: myactuator_rmd_py.ActuatorInterface) -> int
 |  
 |  getVersionDate(...)
 |      getVersionDate(self: myactuator_rmd_py.ActuatorInterface) -> int
 |  
 |  lockBrake(...)
 |      lockBrake(self: myactuator_rmd_py.ActuatorInterface) -> None
 |  
 |  releaseBrake(...)
 |      releaseBrake(self: myactuator_rmd_py.ActuatorInterface) -> None
 |  
 |  reset(...)
 |      reset(self: myactuator_rmd_py.ActuatorInterface) -> None
 |  
 |  sendCurrentSetpoint(...)
 |      sendCurrentSetpoint(self: myactuator_rmd_py.ActuatorInterface, arg0: float) -> myactuator_rmd::MotorStatus2
 |  
 |  sendPositionAbsoluteSetpoint(...)
 |      sendPositionAbsoluteSetpoint(self: myactuator_rmd_py.ActuatorInterface, arg0: float, arg1: float) -> myactuator_rmd::MotorStatus2
 |  
 |  sendTorqueSetpoint(...)
 |      sendTorqueSetpoint(self: myactuator_rmd_py.ActuatorInterface, arg0: float, arg1: float) -> myactuator_rmd::MotorStatus2
 |  
 |  sendVelocitySetpoint(...)
 |      sendVelocitySetpoint(self: myactuator_rmd_py.ActuatorInterface, arg0: float) -> myactuator_rmd::MotorStatus2
 |  
 |  setAcceleration(...)
 |      setAcceleration(self: myactuator_rmd_py.ActuatorInterface, arg0: int, arg1: myactuator_rmd::AccelerationType) -> None
 |  
 |  setCanBaudRate(...)
 |      setCanBaudRate(self: myactuator_rmd_py.ActuatorInterface, arg0: myactuator_rmd::CanBaudRate) -> None
 |  
 |  setCanId(...)
 |      setCanId(self: myactuator_rmd_py.ActuatorInterface, arg0: int) -> None
|  setControllerGains(...)
 |      setControllerGains(self: myactuator_rmd_py.ActuatorInterface, arg0: myactuator_rmd::Gains, arg1: bool) -> myactuator_rmd::Gains
 |  
 |  setCurrentPositionAsEncoderZero(...)
 |      setCurrentPositionAsEncoderZero(self: myactuator_rmd_py.ActuatorInterface) -> int
 |  
 |  setEncoderZero(...)
 |      setEncoderZero(self: myactuator_rmd_py.ActuatorInterface, arg0: int) -> None
 |  
 |  setTimeout(...)
 |      setTimeout(self: myactuator_rmd_py.ActuatorInterface, arg0: datetime.timedelta) -> None
 |  
 |  shutdownMotor(...)
 |      shutdownMotor(self: myactuator_rmd_py.ActuatorInterface) -> None
 |  
 |  stopMotor(...)
 |      stopMotor(self: myactuator_rmd_py.ActuatorInterface) -> None
"""
