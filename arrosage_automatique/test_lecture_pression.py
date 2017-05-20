# -*-coding:utf-8-*-

import communication_arduino
import platform
import time

if platform.system() == "Windows":
    PORT = "COM3"
else:
    PORT = "/dev/ttyACM0"
commu = communication_arduino.Communication_Arduino(PORT)

commu.combien_pression()
time.sleep(1)
print(commu.ecouter())