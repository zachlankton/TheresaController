import os
from pprint import pprint

data = open("data.dat", "rb")
size = os.stat("data.dat").st_size



def readLine(fileObj):
	line = bytearray(fileObj.read(34))
	
	pretty_data = ""
	
	for i in range(0, 16):
		number = line[ i*2 ] << 8 | line[ i*2+1 ]
		pretty_data += str(number) + "\t"
	
	return (pretty_data)




for x in range(0, size+34, 34):
	
	print(readLine(data))
	
print ("Last Line")
data.seek(-34, 2);
print(readLine(data))

data.close()


