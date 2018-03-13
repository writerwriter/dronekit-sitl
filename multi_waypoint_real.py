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
import Mission
import random
import picamera

if __name__ == '__main__':
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
				
				for waypoint_mission in next_multi_mission:
					pm25_sensor = int(waypoint_mission.pm25_sensor)
					video_sensor = int(waypoint_mission.video_sensor)
					photo_sensor = int(waypoint_mission.photo_sensor)

					if waypoint_counter == 0:
						Drone.arm_and_takeoff(vehicle, 7)
						print("set groundspeed to 5m/s.")
						vehicle.airspeed = 5
					Drone.goto_gps(vehicle,waypoint_mission.latitude, waypoint_mission.mission_longitude, 7, logFile, photo_sensor, pm25_sensor, video_sensor)
					time.sleep(5)
					waypoint_counter += 1

				sql.TaskDone(db, next_multi_mission, False)
				print "Setting RTL mode..."
				vehicle.mode = VehicleMode("RTL")

			elif check is 'n':
				next_multi_mission = sql.getNextMission(db, next_multi_mission[0].mission_id)
				sql.TaskDone(db, next_multi_mission, True)
			print "last Task is %s" % sql.findResultMaxId(db)
	print ""
	print "All Task Done !"
	sql.closeDatabase(db)

	print "Close vehicle object"
	vehicle.close()







