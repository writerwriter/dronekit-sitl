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

Drone.arm_and_takeoff(vehicle, 3)

print "start positioning..."

msg_Anchor0 = Drone.return_send_ned_velocity_mavlink_msg(vehicle,0.3,0,0)
msg_Anchor0_inverse = Drone.return_send_ned_velocity_mavlink_msg(vehicle,-0.3,0,0)
msg_Anchor1 = Drone.return_send_ned_velocity_mavlink_msg(vehicle,-0.15,0.26,0)
msg_Anchor1_inverse = Drone.return_send_ned_velocity_mavlink_msg(vehicle,0.15,-0.26,0)
msg_Anchor2 = Drone.return_send_ned_velocity_mavlink_msg(vehicle,-0.15,-0.26,0)
msg_Anchor2_inverse = Drone.return_send_ned_velocity_mavlink_msg(vehicle,0.15,0.26,0)
			
while True:
	offset = 30
	report = Get_uwb_position.Get_uwb_distance()
	print report[0]
	print report[1]
	print report[2]
	if abs(report[0]-report[1]) < offset and abs(report[0]-report[2]) < offset and abs(report[1]-report[2]) < offset:
		print "reach target"
		break
	elif report[0] > report[1] and report[0] > report[2]:
		if abs(report[0]-report[1]) < offset:
			print "go to anchor 2 inverse"
			vehicle.send_mavlink(msg_Anchor2_inverse)
		elif abs(report[0]-report[2]) < offset:
			print "go to anchor 1 inverse"
			vehicle.send_mavlink(msg_Anchor1_inverse)
		else:
			print "go to anchor 0"
			vehicle.send_mavlink(msg_Anchor0)
	elif report[1] > report[0] and report[1] > report[2]:
		if abs(report[1]-report[0]) < offset:
			print "go to anchor 2 inverse"
			vehicle.send_mavlink(msg_Anchor2_inverse)
		elif abs(report[1]-report[2]) < offset:
			print "go to anchor 0 inverse"
			vehicle.send_mavlink(msg_Anchor0_inverse)
		else:
			print "go to anchor 1"
			vehicle.send_mavlink(msg_Anchor1)
	elif report[2] > report[0] and report[2] > report[1]:
		if abs(report[2]-report[0]) < offset:
			print "go to anchor 1 inverse"
			vehicle.send_mavlink(msg_Anchor1_inverse)
		elif abs(report[2]-report[1]) < offset:
			print "go to anchor 0 inverse"
			vehicle.send_mavlink(msg_Anchor0_inverse)
		else:
			print "go to anchor 2"
			vehicle.send_mavlink(msg_Anchor2)
	time.sleep(1)


vehicle.mode = VehicleMode("LAND")


vehicle.close()

