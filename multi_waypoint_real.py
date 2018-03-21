import Drone
import sql
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
import time
import math
from droneapi.lib import Location
import argparse
import g3
import MySQLdb
import camera_control as cc
import Mission
import random
import picamera
import folder_transfer as ftransfer

if __name__ == '__main__':
	#pm25 connect
	air = g3.g3sensor()
	#camera connect
	camera = picamera.PiCamera()
	#connect to vehicle
	parser = argparse.ArgumentParser()
	parser.add_argument('--connect', default='/dev/serial0')
	args = parser.parse_args()

	vehicle = connect(args.connect, baud=57600, wait_ready=True)
	#open log file
	logFile=open("log_multi_waypoint.txt","a+")

	#connect to mysql
	db = MySQLdb.connect(host="120.126.145.102",user="drone",passwd="dronemysql",db="106project")
	#get the last mission id that had been done
	Id = sql.findResultMaxId(db)
	print "Last Task is %s" % Id
	#get the final mission object
	next_multi_mission = sql.getNextMission(db,str(int(Id)-1))

	
	while True:
		sql.closeDatabase(db)
		db = MySQLdb.connect(host="120.126.145.102",user="drone",passwd="dronemysql",db="106project")
		if sql.findResultMaxId(db) < sql.findMissionMaxId(db):
			sql.printTask(db, sql.findResultMaxId(db))

			check = raw_input("you want to fly?(Y/n)")
			if check is 'Y':
				waypoint_counter = 0
				next_multi_mission = sql.getNextMission(db, next_multi_mission[0].mission_id)
				sql.printTask(db, sql.findResultMaxId(db))
				Mission_number = next_multi_mission[0].mission_id
				print "Mission number is %d" % Mission_number
				ftransfer.making_direc(str(Mission_number))
				for waypoint_mission in next_multi_mission:
					pm25_sensor = int(waypoint_mission.pm25_sensor)
					video_sensor = int(waypoint_mission.video_sensor)
					photo_sensor = int(waypoint_mission.photo_sensor)
					print "Sensor:"
					print "pm2.5:%d  video:%d  photo:%d" % pm25_sensor,video_sensor,photo_sensor
					if waypoint_counter == 0:
						Drone.arm_and_takeoff(vehicle, 7)
						print "set groundspeed to 5m/s."
						vehicle.airspeed = 5
					Drone.goto_gps(vehicle,waypoint_mission.mission_latitude, waypoint_mission.mission_longitude, 7, logFile)
					pmdata = air.gsleep(air,5)
					
					waypoint_mission.set_pm25_data(pmdata)
					if photo_sensor == 1:
						cc.capture(camera,str(Mission_number),str(waypoint_counter))
						print " point %d picture : success" % waypoint_counter
					waypoint_counter += 1
				
				sql.TaskDone(db, next_multi_mission, False)
				print "Setting RTL mode..."
				vehicle.mode = VehicleMode("RTL")
				uploader = raw_input("Task is Done,do you want to upload the data ?(Y/n)")
				if uploader is 'Y':
					if ftransfer.fileCount(str(Mission_number)) > 0:
						ftransfer.transfer(str(Mission_number))
						print "Finish upload..( %d photos )" % ftransfer.fileCount(str(Mission_number))
				elif uploader is 'n':
					print "Finish..."
			elif check is 'n':
				next_multi_mission = sql.getNextMission(db, next_multi_mission[0].mission_id)
				sql.TaskDone(db, next_multi_mission, True)
			print "last Task is %s" % sql.findResultMaxId(db)
	camera.close()
	print ""
	print "All Task Done !"
	sql.closeDatabase(db)
	
	print "Close vehicle object"
	vehicle.close()

