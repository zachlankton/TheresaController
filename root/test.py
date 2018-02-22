import urllib2
import time
import os
import serial
from pprint import pprint
import subprocess
from subprocess import Popen


pwr = Popen(['ps | grep "python /root/pwr_meter/tSerial.py"'], shell=True, stdout=subprocess.PIPE).communicate()[0].split("\n")
server = Popen(['ps | grep "python /root/server/main.py"'], shell=True, stdout=subprocess.PIPE).communicate()[0].split("\n")
shots = Popen(['ps | grep "python /root/shot_counter/shot_counter.py"'], shell=True, stdout=subprocess.PIPE).communicate()[0].split("\n")

pprint( len(pwr) );
pprint( len(server) );
pprint( len(shots) );
