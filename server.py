from flask import Flask
from megapi import *


class FourWheelDriveCar():
    # 支持六个车轱辘

    def __init__(self, port):
        self.PowerModule = MegaPi()
        self.PowerModule.start(port)
        self.MotorReset()
        self.ServoReset()
        self.test()

    # config = configparser.ConfigParser()
    # config.read("config.ini")
    # self.LEFT_1 = config.getint("car", "LEFT_1")

    # 重置
    # 舵机角度初始化
    def ServoReset(self):
        print("init")
        self.PowerModule.servoRun(8, 1, 90)
        self.PowerModule.servoRun(8, 1, 90)
        self.PowerModule.servoRun(8, 2, 90)
        self.PowerModule.servoRun(8, 2, 90)
        self.PowerModule.servoRun(7, 1, 90)
        self.PowerModule.servoRun(7, 1, 90)
        self.PowerModule.servoRun(7, 2, 90)
        self.PowerModule.servoRun(7, 2, 90)
        self.PowerModule.servoRun(6, 1, 90)
        self.PowerModule.servoRun(6, 1, 90)
        self.PowerModule.servoRun(6, 2, 90)
        self.PowerModule.servoRun(6, 2, 90)

        # 将所有电机速度清零
    def test(self):
        self.forward()
        sleep(1)
        self.backward()
        sleep(1)
        self.turnLeft()
        sleep(1)
        self.turnRight()
        sleep(1)
        self.MotorReset()
        sleep(1)
        self.ServoReset()
        sleep(1)
    def MotorReset(self):
        print("reset")
        self.PowerModule.motorRun(1, 0)
        self.PowerModule.motorRun(9, 0)
        self.PowerModule.motorRun(2, 0)
        self.PowerModule.motorRun(10, 0)
        self.PowerModule.motorRun(3, 0)
        self.PowerModule.motorRun(11, 0)

    # 前进
    def forward(self):
        print("forward")
        self.MotorReset()
        self.PowerModule.motorRun(1, 50)
        self.PowerModule.motorRun(9, 50)
        self.PowerModule.motorRun(2, 50)
        self.PowerModule.motorRun(10, 50)
        self.PowerModule.motorRun(3, 50)
        self.PowerModule.motorRun(11, 50)

    # 后退
    def backward(self):
        print("backward")
        self.MotorReset()
        self.PowerModule.motorRun(1, -50)
        self.PowerModule.motorRun(9, -50)
        self.PowerModule.motorRun(2, -50)
        self.PowerModule.motorRun(10, -50)
        self.PowerModule.motorRun(3, -50)
        self.PowerModule.motorRun(11, -50)

    # 左转
    def turnLeft(self):
        print("left")
        self.MotorReset()
        LeftInitAngle = 90
        LeftAngle = LeftInitAngle + 5
        self.PowerModule.servoRun(8, 1, LeftAngle)

        self.PowerModule.servoRun(8, 2, LeftAngle)

        self.PowerModule.servoRun(7, 1, LeftAngle)

        self.PowerModule.servoRun(7, 2, LeftAngle)

        self.PowerModule.servoRun(6, 1, LeftAngle)

        self.PowerModule.servoRun(6, 2, LeftAngle)

    # 右转
    def turnRight(self):
        print("right")
        self.MotorReset()
        RightInitAngle = 90
        RightAngle = RightInitAngle - 5
        self.PowerModule.servoRun(8, 1, RightAngle)
        self.PowerModule.servoRun(8, 2, RightAngle)
        self.PowerModule.servoRun(7, 1, RightAngle)
        self.PowerModule.servoRun(7, 2, RightAngle)
        self.PowerModule.servoRun(6, 1, RightAngle)
        self.PowerModule.servoRun(6, 2, RightAngle)

    def stop(self):
        print("stop")
        self.MotorReset()
        self.ServoReset()


server = Flask(__name__)


@server.route("/car/control/<int:act>", methods=["GET"])
def car_control(act: int):
    if act == 1:
        car.forward()  # 参数1为前进
        return "1"
    if act == 2:
        car.backward()  # 参数2为后退
        return "1"
    if act == 3:
        car.turnLeft()  # 参数3为左转
        return "1"
    if act == 4:
        car.turnRight()  # 参数4为右转
        return "1"
    if act == 0:
        car.stop()  # 参数0为停车
        return "1"
    else:
        return "-1"


if __name__ == "__main__":
    car = FourWheelDriveCar('/dev/ttyUSB0')

    PORT_NUM = 8899  # 后端监听端口
    server.run("0.0.0.0",port=PORT_NUM, debug=True)
    print('Exit...')
    car.stop()
    car.PowerModule.close()
    print("Stopped")
    sleep(3)
