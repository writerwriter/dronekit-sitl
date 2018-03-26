import os
print len([name for name in os.listdir('/Users/wuchengru/Desktop/dronekit-sitl/dronekit-sitl/picture/MISSION_7') if os.path.isfile(name)])