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

NORTH = 0.5
SOUTH = -0.5

EAST = 0.5
WEST = -0.5

UP = -0.5
DOWN = 0.5

DURATION = 2
print vehicle.location.global_relative_frame

Drone.send_ned_velocity(vehicle, NORTH, 0, 0, DURATION)
Drone.send_ned_velocity(vehicle, 0, 0, 0, 1)

print vehicle.location.global_relative_frame

vehicle.close()



