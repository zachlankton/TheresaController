#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
from pprint import pprint
from os import listdir
from os.path import isfile, join
import os

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
       
        if (self.path == "/"): loadIndex(self)
        elif (self.path == "/list_hb_data"): listHBData(self)
        elif (self.path.find("/hb_data/") > -1): loadHBData(self)
        elif (self.path == "/tail"): getLastMinute(self)
        elif (self.path == "/tail10"): getLast10Minute(self)
        elif (self.path == "/shotlog"): loadShotLog(self)
        elif (self.path.find("/shotlog/") > -1): loadShotLogFromDate(self)
        else: load404(self)

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def loadIndex(self):
	fi = open("/root/server/index.html")
	self._set_headers()
	self.wfile.write(fi.read())
	

def getLast10Minute(self):
	files = getHBDataList()
	fLen = len(files)
	lastFile = open("/root/pwr_meter/data/" + files[fLen - 1])
	curFile = open("/root/pwr_meter/data.dat")
	newFile = lastFile.read() + curFile.read()
	
	lastFile.close()
	curFile.close()
	
	self.send_response(200)
	self.send_header('Content-type', 'text/plain')
	self.end_headers()
	self.wfile.write(newFile[-20400:])
	

def listHBData(self):
	onlyfiles = getHBDataList()
	for x in range(0, len(onlyfiles)):
		onlyfiles[x] = "<a href=\"/hb_data/"+onlyfiles[x]+"\">"+onlyfiles[x]+"</a><br>"
	text = "\n".join(onlyfiles)
	self.send_response(200)
	self.send_header('Content-type', 'text/html')
	self.end_headers()
	self.wfile.write(text)
	
def getHBDataList():
	mypath = "/root/pwr_meter/data"
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	onlyfiles.sort(key=long)
	return onlyfiles
	
def loadHBData(self):
	filename = self.path[9:]
	if len(filename) == 0:
		onlyfiles = getHBDataList()
		text = "\n".join(onlyfiles)
		self.send_response(200)
		self.send_header('Content-type', 'text/plain')
		self.end_headers()
		self.wfile.write(text)
		return 0
	elif (filename == "data.dat"):
		data = open("/root/pwr_meter/data.dat")
	else:
		data = open("/root/pwr_meter/data/" + filename)
		
	self.send_response(200)
	self.send_header('Content-type', 'application/octet-stream')
	self.end_headers()
	self.wfile.write(data.read())
	data.close()
	
def loadShotLog(self):
	f = open("/root/shot_counter/log.txt")
	
	self.send_response(200)
	self.send_header('Content-type', 'text/plain')
	self.end_headers()
	
	self.wfile.write(f.read())
	f.close()
	

def loadShotLogFromDate(self):
        filename = self.path[9:]
        f = open("/root/shot_counter/archive/" + filename)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        self.wfile.write(f.read())
        f.close()
        
def load404(self):
	self._set_headers()
	self.wfile.write("404")

def run(server_class=HTTPServer, handler_class=S, port=800):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

def getLastMinute(self):
	self.send_response(200)
	self.send_header('Content-type', 'text/plain')
	self.end_headers()
	self.wfile.write(getLastMinuteOfData()) 
    
def getLastMinuteOfData():
	data = open("/root/pwr_meter/data.dat", "rb")
	data.seek(-2040, 2);
	
	dataStr = ""
	
	for x in range(0, 2040, 34):
		
		dataStr += readLine(data) + "\n"
	
	data.close()
	return dataStr
	
def readLine(fileObj):
	line = bytearray(fileObj.read(34))
	
	pretty_data = ""
	
	for i in range(0, 16):
		number = line[ i*2 ] << 8 | line[ i*2+1 ]
		pretty_data += str(i+1) + ":" + str(number) + "\t"
	
	return (pretty_data)
	

if __name__ == "__main__":
	
	run()
        
        
        
        
        
        
        
        
        
