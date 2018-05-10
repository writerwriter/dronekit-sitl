import Drone
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
import time
import math
from droneapi.lib import Location
import argparse
import Mission
import random
import Get_uwb_position
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='/dev/serial0')
args = parser.parse_args()

vehicle = connect(args.connect, baud=57600, wait_ready=True)

logFile=open("log_velocity.txt","a+")

Drone.arm_and_takeoff(vehicle, 5)

NORTH = 0.3
SOUTH = -0.3

EAST = 0.3
WEST = -0.3

UP = -0.5
DOWN = 0.5

DURATION = 10

msg = Drone.return_send_ned_velocity_mavlink_msg(vehicle,SOUTH,0,0)
msg2 = Drone.return_send_ned_velocity_mavlink_msg(vehicle,NORTH,0,0)


print vehicle.location.global_relative_frame
starttime = time.time()
endtime = time.time()

Drone.

vehicle.mode = VehicleMode("LAND")


vehicle.close()



