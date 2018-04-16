import serial
import struct
import time

def Get_uwb_position():
	SERIAL_PORT = '/dev/ttyUSB0'
	ser = serial.Serial(SERIAL_PORT,115200)
	ser.timeout = None

	vector = []
	
	count = 0
	flag = 0
	while True:
		print "before read"
		data_string = ser.read(1)
		print data_string.encode('hex')
		while data_string == '\xFF':
			print "hello1"
			data_string = ser.read(2)
			report_x = int(data_string[0:1].encode('hex'),16)*100 + int(data_string[1:2].encode('hex'),16)
			data_string = ser.read(2)
			report_y = int(data_string[0:1].encode('hex'),16)*100 + int(data_string[1:2].encode('hex'),16)
			data_string = ser.read(2)
			report_z = int(data_string[0:1].encode('hex'),16)*100 + int(data_string[1:2].encode('hex'),16)
			vector.append([report_x,report_y,report_z])
			count += 1
			if count >= 10:
				flag = 1
				break
			data_string = ser.read(1)
		if flag == 1:
			break
	average = [0,0,0]
	for v in vector:
		average[0] += v[0]
		average[1] += v[1]
		average[2] += v[2]
	average[0] /= count;
	average[1] /= count;
	average[2] /= count;
	print "done with work"
	ser.close()
	return average

if __name__ == "__main__":
	report = Get_uwb_position()
	print report[0]
	print report[1]
	print report[2]

