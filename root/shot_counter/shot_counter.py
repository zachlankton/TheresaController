import os
import datetime
import time
from pprint import pprint
import wiringpi
wiringpi.wiringPiSetup()


# shotTrigger = onionGpio.OnionGpio(3)
# status = shotTrigger.setInputDirection()
# if (status != 0): exit("Cannot Set Pin 3 to Input Mode")

signal = 0
def main():
	# shotTrig = wiringpi.digitalRead(9)
	print ("Running!")
	
	while(1):
	
		# wait for the value to go low
		while (int(wiringpi.digitalRead(9) ) == 1): time.sleep(0.1)
		time.sleep(0.05) #debounce falling edge
		
		# make sure we have a solid signal before we write the time stamp
		signalLow = True
		for x in range(0,10):
			if ( int( wiringpi.digitalRead(9) ) == 1): 
				signalLow = False
				break
			time.sleep(0.01)
			
		if (signalLow == True): writeTimeStamp()
		
		# wait for the value to go high
		while (int( wiringpi.digitalRead(9) ) == 0): time.sleep(0.1) 
		time.sleep(0.1) #debounce rising edge


def writeTimeStamp():
	rightNow = datetime.datetime.now()
	
	timeStamp = ""
	timeStamp += str(rightNow.year)
	timeStamp += str(rightNow.month).rjust(2, "0")
	timeStamp += str(rightNow.day).rjust(2, "0")
	timeStamp += str(rightNow.hour).rjust(2, "0") 
	timeStamp += str(rightNow.minute).rjust(2, "0") 
	timeStamp += str(rightNow.second).rjust(2, "0")

	f = open("/root/shot_counter/log.txt", "a")
	f.write(timeStamp + "\n")
	f.close()
	
main()




