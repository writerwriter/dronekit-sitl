import Drone
import sql
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
import time
import math
from droneapi.lib import Location
import argparse
#import g3
import MySQLdb
import Mission
import random
#import picamera

if __name__ == '__main__':
	#camera connect
	#camera = picamera.PiCamera()
	#connect to vehicle
	parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
	parser.add_argument('--connect', 
	                   help="Vehicle connection target string. If not specified, SITL automatically started and used.")
	args = parser.parse_args()

	connection_string = args.connect
	sitl = None
	#Start SITL if no connection string specified
	if not connection_string:
	    import dronekit_sitl
	    sitl = dronekit_sitl.start_default()
	    connection_string = sitl.connection_string()
	# Connect to the Vehicle
	print 'Connecting to vehicle on: %s' % connection_string
	vehicle = connect(connection_string, wait_ready=True)

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

			check = raw_input("you want to fly or search again?(Y/n/r)")
			if check is 'Y':
				waypoint_counter = 0
				next_multi_mission = sql.getNextMission(db, next_multi_mission[0].mission_id)
				
				for waypoint_mission in next_multi_mission:
					pm25_sensor = int(waypoint_mission.pm25_sensor)
					video_sensor = int(waypoint_mission.video_sensor)
					photo_sensor = int(waypoint_mission.photo_sensor)
					point_staytime = int(waypoint_mission.mission_staytime)
					point_height = int(waypoint_mission.mission_height)
					waypoint_mission.set_point_num(waypoint_counter+1)
					if waypoint_counter == 0:
						Drone.arm_and_takeoff(vehicle, point_height)
						print "set groundspeed to 5m/s."
						vehicle.airspeed = 5
					Drone.goto_gps(vehicle,waypoint_mission.mission_latitude, waypoint_mission.mission_longitude, point_height, logFile)
					time.sleep(point_staytime)
					waypoint_mission.set_pm25_data(-1)
					waypoint_counter += 1

				sql.TaskDone(db, next_multi_mission, False)
				print "Setting RTL mode..."
				vehicle.mode = VehicleMode("RTL")

			elif check is 'n':
				next_multi_mission = sql.getNextMission(db, next_multi_mission[0].mission_id)
				sql.TaskDone(db, next_multi_mission, True)
			elif check is 'r':
				continue
			print "last Task is %s" % sql.findResultMaxId(db)
	print ""
	print "All Task Done !"
	sql.closeDatabase(db)

	print "Close vehicle object"
	vehicle.close()





