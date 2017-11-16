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

while True:
        print str(vehicle.battery)+'\n'
        time.sleep(1)

vehicle.close()
