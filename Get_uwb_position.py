import serial
import struct
import time

def Check_sum(pdata,len):
	sum = 0
	for i in range(len):
		sum+=int(pdata[i].encode('hex'),16)
	sum = ~sum
	return sum

def Get_uwb_position():
	SERIAL_PORT = '/dev/ttyUSB0'
	ser = serial.Serial(SERIAL_PORT,115200)
	ser.timeout = None

	vector = []
	
	count = 0
	flag = 0
	debug = True
	while True:
		ser.flushInput()
		data_string = ser.read(48)
		print data_string.encode('hex')
		while data_string[0:2] == '\xD6\x6D':
			if(debug or Check_sum(data_string[2:27],25) == int(data_string[46:48].encode('hex'),16)):
				report_x = int(data_string[14:15].encode('hex'),16)+int(data_string[15:16].encode('hex'),16)*16
				report_y = int(data_string[16:17].encode('hex'),16)+int(data_string[17:18].encode('hex'),16)*16
				report_z = int(data_string[18:19].encode('hex'),16)+int(data_string[19:20].encode('hex'),16)*16
				vector.append([report_x,report_y,report_z])

				posx=int(data_string[6:7].encode('hex'),16)+int(data_string[7:8].encode('hex'),16)*16
				posy=int(data_string[8:9].encode('hex'),16)+int(data_string[9:10].encode('hex'),16)*16
				posz=int(data_string[10:11].encode('hex'),16)+int(data_string[11:12].encode('hex'),16)*16

				#print "%d,%d,%d" % (posx,posy,posz)
				
				count += 1
				if count >= 10:
					flag = 1
					break
			data_string = ser.read(48)
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
	while True:
		report = Get_uwb_position()
		print report[0]
		print report[1]
		print report[2]

