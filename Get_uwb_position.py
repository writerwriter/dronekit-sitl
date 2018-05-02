import serial
import struct
import time
import math

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
				report_x = int(data_string[14:15].encode('hex'),16)+int(data_string[15:16].encode('hex'),16)*256
				report_y = int(data_string[16:17].encode('hex'),16)+int(data_string[17:18].encode('hex'),16)*256
				report_z = int(data_string[18:19].encode('hex'),16)+int(data_string[19:20].encode('hex'),16)*256
				vector.append([report_x,report_y,report_z])

				posx=int(data_string[6:7].encode('hex'),16)+int(data_string[7:8].encode('hex'),16)*256
				posy=int(data_string[8:9].encode('hex'),16)+int(data_string[9:10].encode('hex'),16)*256
				posz=int(data_string[10:11].encode('hex'),16)+int(data_string[11:12].encode('hex'),16)*256
				#print posx
				#print posy
				#print posz

				#print "%d,%d,%d" % (posx,posy,posz)

				#a1_x = int(data_string[26:27].encode('hex'),16)+int(data_string[27:28].encode('hex'),16)*256
				#a1_y = int(data_string[28:29].encode('hex'),16)+int(data_string[29:30].encode('hex'),16)*256
				#a1_z = int(data_string[30:31].encode('hex'),16)+int(data_string[31:32].encode('hex'),16)*256

				#print "%d,%d,%d" % (a1_x,a1_y,a1_z)
				
				count += 1
				if count >= 10:
					flag = 1
					break
			data_string = ser.read(48)
			print data_string.encode('hex')
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
		#print "go North %f m, go East %f m" % ((500-report[1])/100.0,(5*math.pow(3,0.5)*100-report[0])/100.0)
		#Drone.send_ned_velocity((500-report[1])/200.0,(5*math.pow(3,0.5)*100-report[0])/200.0,0,2)
		time.sleep(1)
		#result = Get_uwb_location.Get_uwb_location()
		#if math.fabs(500-result[1]) < 30 && math.fabs(5*math.pow(3,0.5)*100-result[0]) < 30:
		#	break
