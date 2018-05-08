import Drone
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
import time
import math
from droneapi.lib import Location
import argparse
import Mission
import random

parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='/dev/serial0')
args = parser.parse_args()

vehicle = connect(args.connect, baud=57600, wait_ready=True)

logFile=open("log_velocity.txt","a+")

Drone.arm_and_takeoff(vehicle, 5)

NORTH = 0.3
SOUTH = -0.3

EAST = 0.1
WEST = -0.1

UP = -0.5
DOWN = 0.5

DURATION = 15

msg = Drone.return_send_ned_velocity_mavlink_msg(vehicle,SOUTH,0,0)
msg2 = Drone.return_send_ned_velocity_mavlink_msg(vehicle,NORTH,0,0)


print vehicle.location.global_relative_frame
starttime = time.time()
endtime = time.time()
while True:
	if endtime-starttime <= 15:
		vehicle.send_mavlink(msg)
	elif endtime-starttime > 15 and endtime-starttime <= 30:
		vehicle.send_mavlink(msg2)
	elif endtime-starttime > 30:
		break
	endtime = time.time()
	time.sleep(1)

#Drone.send_ned_velocity(vehicle, SOUTH, 0, 0, DURATION)

print vehicle.location.global_relative_frame

time.sleep(5)

vehicle.mode = VehicleMode("LAND")


vehicle.close()



