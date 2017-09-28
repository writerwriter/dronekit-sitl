from dronekit import connect, VehicleMode,LocationGlobalRelative
from pymavlink import mavutil
import time
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='/dev/serial0')
args = parser.parse_args()

vehicle = connect(args.connect, baud=57600, wait_ready=True)
#print "Battery: %s" % vehicle.battery
#print "Armed: %s" % vehicle.armed
#print "System status: %s" % vehicle.system_status.state

def condition_yaw(heading, relative=False):
    if relative:
        is_relative=1 #yaw relative to direction of travel
    else:
        is_relative=0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)
    vehicle.flush()

def arm_and_takeoff(aTargetAltitude):
        print "Basic pre-arm checks"
        while not vehicle.is_armable:
                print " Waiting for vehicle to initialise..."
                time.sleep(1)
        print "Arming motors"
        #Copter should arm in GUIDED mode
        vehicle.mode = VehicleMode("GUIDED")
        vehicle.armed = True
        while not vehicle.armed:
                print " Waiting for arming..."
                time.sleep(1)

        print "Taking off!"
        vehicle.simple_takeoff(aTargetAltitude)

        while True:
                print " Altitude: ", vehicle.location.global_relative_frame.alt
                if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
                        print "Reached target altitude"
                        break
                time.sleep(1)

arm_and_takeoff(2)
sleep(10)
print "takeoff and hover complete"
condition_yaw(180)
print "turn 180 degrees complete"
sleep(20)

print "Mission complete! Time to land~"
vehicle.mode=VehicleMode("LAND")


vehicle.close()
