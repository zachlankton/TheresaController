import os
import datetime
from pprint import pprint

rightNow = datetime.datetime.now()

fileName = ""
fileName += str(rightNow.year)
fileName += str(rightNow.month).rjust(2, "0")
fileName += str(rightNow.day).rjust(2, "0")
fileName += str(rightNow.hour).rjust(2, "0") 
fileName += str(rightNow.minute).rjust(2, "0") 
fileName += str(rightNow.second).rjust(2, "0")

os.rename("/root/pwr_meter/data.dat", "/root/pwr_meter/data/" + fileName);