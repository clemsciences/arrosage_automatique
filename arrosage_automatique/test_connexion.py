# -*-coding:utf-8-*-
__author__ = 'spraakforskaren'

import time
import communication_arduino as ca
import platform
if platform.system() == "Windows":
    PORT = "COM3"
else:
    PORT = "/dev/ttyACM0"
#try:
commu = ca.Communication_Arduino(PORT)

commu.demander_si_bonne_reception("beth")

time.sleep(2)
print commu.ecouter()
