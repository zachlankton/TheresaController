import serial
from pprint import pprint

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
print("Running!")
while(1):
	s = ser.read(34)
	s = bytearray(s)

	#valStr = ""
	#for x in range(0, 17):
	#	i = s[x*2] << 8 | s[x*2+1]
	#	valStr += (str(x+1) + ":" + str(i) + "\t" )
	
	fo = open("/root/pwr_meter/data.dat", "ab")
	fo.write(s)
	fo.close()

ser.close()
