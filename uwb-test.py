import serial
import struct
import time

if __name__ == '__main__':
	SERIAL_PORT = '/dev/ttyUSB0'
	ser = serial.Serial(SERIAL_PORT,115200)
	ser.timeout = None

	ranges = []
	anchors = []
	transforms = []
	beacon_count = 0	

	while True:
		data_string = ser.read(2)
		while data_string == '\xFF\xFF':
			print "success"
			data_string = ser.read(3)
			result_x = int(data_string[0:1].encode('hex'),16) + int(data_string[1:2].encode('hex'),16)/100.0 +  int(data_string[2:3].encode('hex'),16)/10000.0
			print result_x
			
                        data_string = ser.read(3)
                        result_y = int(data_string[0:1].encode('hex'),16) + int(data_string[1:2].encode('hex'),16)/100.0 +  int(data_string[2:3].encode('hex'),16)/10000.0
                        print result_y
			
			data_string = ser.read(3)
                        result_z = int(data_string[0:1].encode('hex'),16) + int(data_string[1:2].encode('hex'),16)/100.0 +  int(data_string[2:3].encode('hex'),16)/10000.0
                        print result_z
			
			data_string = ser.read(2)

