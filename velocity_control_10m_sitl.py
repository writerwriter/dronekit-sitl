import Drone
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
import time
import math
from droneapi.lib import Location
import argparse
import Mission
import random

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


logFile=open("log_velocity.txt","a+")

Drone.arm_and_takeoff(vehicle, 5)

NORTH = 0.2
SOUTH = -0.1

EAST = 0.2
WEST = -0.1

UP = -0.5
DOWN = 0.5

DURATION = 10
print vehicle.location.global_relative_frame

starttime = time.time()
msg1 = Drone.return_send_ned_velocity_mavlink_msg(vehicle, NORTH, 0, 0)
msg2 = Drone.return_send_ned_velocity_mavlink_msg(vehicle, 0, EAST, 0)
while True:
	print str(vehicle.velocity)
	temptime = time.time()
	if temptime-starttime < 5:
		vehicle.send_mavlink(msg1)
	elif temptime-starttime >= 5 and temptime-starttime < 10:
		vehicle.send_mavlink(msg2)
	elif temptime-starttime >= 10:
		break
endtime = time.time()
print vehicle.location.global_relative_frame
print endtime-starttime

vehicle.close()



