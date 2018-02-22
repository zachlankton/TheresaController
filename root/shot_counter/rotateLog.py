import os
import datetime
import sys
from subprocess import call
from pprint import pprint

rightNow = datetime.datetime.now()

fileName = ""
fileName += str(rightNow.year)
fileName += str(rightNow.month).rjust(2, "0")
fileName += str(rightNow.day).rjust(2, "0")

#because the file will run once a day anyway.... lets rotate some service logs while we're here
call( ["cat /root/pwr_meter/stdout.txt > /root/pwr_meter/stdout.archive/" + fileName], shell=True)
call( ["cat /root/server/stdout.txt > /root/server/stdout.archive/" + fileName], shell=True)
call( ["cat /root/shot_counter/stdout.txt > /root/shot_counter/stdout.archive/" + fileName], shell=True)

call(["cat /dev/null > /root/pwr_meter/stdout.txt"], shell=True)
call(["cat /dev/null > /root/server/stdout.txt"], shell=True)
call(["cat /dev/null > /root/shot_counter/stdout.txt"], shell=True)

#if the log file is empty then no need to rotate
logSize = os.stat("/root/shot_counter/log.txt").st_size
if (logSize == 0): sys.exit()

# if file already exists then do not overwrite it
if ( os.path.isfile("/root/shot_counter/archive/" + fileName) ):
	sys.exit();

os.rename("/root/shot_counter/log.txt", "/root/shot_counter/archive/" + fileName);
open("/root/shot_counter/log.txt", 'a').close()

