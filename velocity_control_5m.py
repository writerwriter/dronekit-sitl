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

NORTH = 0.1
SOUTH = -0.1

EAST = 0.1
WEST = -0.1

UP = -0.5
DOWN = 0.5

DURATION = 3
print vehicle.location.global_relative_frame

Drone.send_ned_velocity(vehicle, NORTH, 0, 0, DURATION)
Drone.send_ned_velocity(vehicle, 0, 0, 0, 1)

print vehicle.location.global_relative_frame

vehicle.close()



