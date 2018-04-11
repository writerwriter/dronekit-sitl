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

				daytimes = time.strftime("%Y-%m-%d",time.localtime())
				logFile=open("./log_file/"+daytimes+"_MISSION_"+str(Mission_number)+".txt","a+")


				ftransfer.making_direc(str(Mission_number))
				for waypoint_mission in next_multi_mission:
					square_count = 1
					pm25_sensor = int(waypoint_mission.pm25_sensor)
					video_sensor = int(waypoint_mission.video_sensor)
					photo_sensor = int(waypoint_mission.photo_sensor)

					logFile.write("Points  "+str(waypoint_counter)+":"+"\n")
					print "Sensor:"
					print "pm2.5:%d  video:%d  photo:%d" % (pm25_sensor,video_sensor,photo_sensor)
					if waypoint_counter == 0:
						Drone.arm_and_takeoff(vehicle, 7)
						print "set groundspeed to 5m/s."
						vehicle.airspeed = 5
					Drone.goto_gps(vehicle,waypoint_mission.mission_latitude, waypoint_mission.mission_longitude, 7, logFile)
					pmdata = air.gsleep(air,5)
					
					waypoint_mission.set_pm25_data(pmdata)
					if photo_sensor == 1:
						Drone.condition_yaw(vehicle,0)
						cc.capture(camera,str(Mission_number),str(waypoint_counter)+"_"+str(square_count))
						print "degree 0 , success"
						Drone.condition_yaw(vehicle,90)
						square_count = square_count+1
						cc.capture(camera,str(Mission_number),str(waypoint_counter)+"_"+str(square_count))
						print "degree 90 , success"
						Drone.condition_yaw(vehicle,180)
						square_count = square_count+1
						cc.capture(camera,str(Mission_number),str(waypoint_counter)+"_"+str(square_count))
						print "degree 180 , success"
						Drone.condition_yaw(vehicle,270)
						square_count = square_count+1
						cc.capture(camera,str(Mission_number),str(waypoint_counter)+"_"+str(square_count))
						print "degree 270 , success"

						print " Point %d picture : success" % waypoint_counter
					waypoint_counter += 1
				
				sql.TaskDone(db, next_multi_mission, False)
				print "Setting RTL mode..."
				vehicle.mode = VehicleMode("RTL")
				if photo_sensor ==1:
					uploader = raw_input("Task is Done,do you want  upload the data ?(Y/n)")
					if uploader is 'Y' :
						ftransfer.transfer(str(Mission_number))
						print "Finish upload.."
					elif uploader is 'n':
						print "Skip the upload step..."
			elif check is 'n':
				next_multi_mission = sql.getNextMission(db, next_multi_mission[0].mission_id)
				for waypoint_mission in next_multi_mission:
					waypoint_mission.set_pm25_data(0)
				sql.TaskDone(db, next_multi_mission, True)
			print "last Task is %s" % sql.findResultMaxId(db)
	camera.close()
	print ""
	print "All Task Done !"
	sql.closeDatabase(db)
	
	print "Close vehicle object"
	vehicle.close()

