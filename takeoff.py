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
time.sleep(10)
print "takeoff and hover complete"
print "Mission complete! Time to land~"
vehicle.mode=VehicleMode("LAND")


vehicle.close()
