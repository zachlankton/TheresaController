import urllib2
import time
import os
import serial
from pprint import pprint
from subprocess import call
from subprocess import Popen

def internet_on():
    try:
        urllib2.urlopen('http://www.google.com', timeout=1)
        return True
    except urllib2.URLError as err: 
        return False


while(internet_on() == False):
	call("wifimanager")
	time.sleep(300)
	
ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(0.1)
ser.close()
	
	
call(["python", "/root/teensy_writer/teensy.py", "restart"])
time.sleep(5)
pwr = Popen(["python /root/pwr_meter/tSerial.py >> /root/pwr_meter/stdout.txt 2>&1"], shell=True)
shots = Popen(["python /root/shot_counter/shot_counter.py >> /root/shot_counter/stdout.txt 2>&1"], shell=True)
server = Popen(["python /root/server/main.py >> /root/server/stdout.txt 2>&1"], shell=True)


while(1):
	if pwr.poll() is not None:
		pwr = Popen(["python /root/pwr_meter/tSerial.py >> /root/pwr_meter/stdout.txt 2>&1"], shell=True)
	if shots.poll() is not None:
		shots = Popen(["python /root/shot_counter/shot_counter.py >> /root/shot_counter/stdout.txt 2>&1"], shell=True)
	if server.poll() is not None:
		server = Popen(["python /root/server/main.py >> /root/server/stdout.txt 2>&1"], shell=True)
	time.sleep(10)
	

