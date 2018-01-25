import Drone
import sql
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
import time
import math
from droneapi.lib import Location
import argparse
import MySQLdb
import Mission
import random

if __name__ == '__main__':
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


	logFile=open("log_gps.txt","a+")

	db = MySQLdb.connect(host="120.126.145.102",user="drone",passwd="dronemysql",db="106project")
	Id = sql.findResultMaxId(db)

	print "Last Task is %s" % Id
	next_mission = sql.getNextMission(db,str(int(Id)-1)) #fianl mission
	
	while True:
		sql.closeDatabase(db)
		db = MySQLdb.connect(host="120.126.145.102",user="drone",passwd="dronemysql",db="106project")
		if sql.findResultMaxId(db) < sql.findMissionMaxId(db):
			sql.printTask(db,sql.findResultMaxId(db))
			#doing mission
			check = raw_input("you want to fly?(Y/n)")
			if check is 'Y':
				next_mission = sql.getNextMission(db,next_mission.mission_id)
				#print "doing things"
				Drone.arm_and_takeoff(vehicle,7)
				print("set groundspeed to 5m/s.")
				vehicle.airspeed = 5
				Drone.goto_gps(vehicle,next_mission.mission_latitude, next_mission.mission_longitude, 7, logFile)
				time.sleep(5)
				next_mission.setPM25(random.randint(1,100))
				sql.TaskDone(db,next_mission,False)
				print "Setting RTL mode..."
				vehicle.mode = VehicleMode("RTL")
			elif check is 'n':
				next_mission = sql.getNextMission(db,next_mission.mission_id)
				sql.TaskDone(db,next_mission,True)
			print "Last Task is %s" % sql.findResultMaxId(db)
	print ""
	print "All Task Done !"
	sql.closeDatabase(db)

	print "Close vehicle object"
	vehicle.close()