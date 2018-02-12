import usb.core
import usb.util
import sys
from pprint import pprint
import time
usleep = lambda x: time.sleep(x/1000000.0)

from intelhex import IntelHex
ih = IntelHex()                     # create empty object
ih.loadhex('blink_slow_Teensy36.hex')               # load from hex

libusb_teensy_handle = None

# Teensy 3.6 code and block size
code_size = 1048576
block_size = 1024
write_size = block_size + 64

def get_block(addr, data):
	if (data == 0):
		data_size=0
	else:
		data_size = len(data)
	buf = ""

	for x in range(0, write_size):
		buf += chr(0);

	buf = bytearray(buf)
	
	# Set Address
	buf[0] = addr & 255
	buf[1] = (addr >> 8) & 255
	buf[2] = (addr >> 16) & 255
	
	if (data_size == 0): return buf
	
	index = 0
	for x in range(64, write_size):
		
		buf[x] = data[index + addr]
		
		index += 1
	
	return buf
	
def reboot():
	print("Rebooting...");
	serialIF = usb.core.find(idVendor=0x16C0, idProduct=0x0483);
	
	if (serialIF is None):
		print ("Can't Find Teensy Serial to Reboot!")
		return 0
		
	if serialIF.is_kernel_driver_active(0):
		serialIF.detach_kernel_driver(0)
		
	reboot_cmd = chr(134);
	response = serialIF.ctrl_transfer(0x21, 0x20, 0, 0, reboot_cmd, 10000)
	
	usb.util.dispose_resources(serialIF)
	
	return response
	

def teensy_close():
	global libusb_teensy_handle
	if (libusb_teensy_handle is not None):
		usb.util.dispose_resources( libusb_teensy_handle )
		libusb_teensy_handle = None

def teensy_open():
	print ("opening connection to teensy halfkay bootloader...")
	global libusb_teensy_handle

	teensy_close();
	
	libusb_teensy_handle = usb.core.find(idVendor=0x16C0, idProduct=0x0478)
	
	if libusb_teensy_handle is None:
		sys.exit("Need to reset teensy!")
		
	if libusb_teensy_handle.is_kernel_driver_active(0):
		libusb_teensy_handle.detach_kernel_driver(0)
		
	print("Connection Successful!")
	
	
def teensy_write(msg, timeout):
	global libusb_teensy_handle
	r = libusb_teensy_handle.ctrl_transfer(0x21, 9, 0x0200, 0, msg, timeout)
	if r >= 0: 
		return 1
	else:
		usleep(10000)
		return 0
	
def boot():
	print ("Booting...")
	
	buf = get_block(0,0);
	buf[0] = chr(255)
	buf[1] = chr(255)
	buf[2] = chr(255)
	
	teensy_write(buf, 500);
	
def main():

	reboot()
	teensy_open()
	print("Writing Teensy!");
	
	for addr in range(0, len(ih), block_size):
		teensy_write( get_block(addr, ih), 5000 if addr==0 else 500 )
	boot()
	teensy_close()
	
	print ("Done!");
	
main()










