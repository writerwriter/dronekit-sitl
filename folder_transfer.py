import picamera
import os
import subprocess as sb


def making_direc(target_path,target_mission_number):
	sb.call(["mkdir",str(target_path+target_mission_number)])
	print "making directory success"

def transfer(target_path,target_folder):
	sb.call(["sshpass","-p","unigrid","scp","-r",target_path+target_folder,"dmcl@120.126.145.102:/var/www/html/dronePicture"])
	print "transfer finish..."
def fileCount(foldername):
	return len([name for name in os.listdir('/drone/dronekit-sitl/picture/mission_'+foldername+"/") if os.path.isfile(name)])

if __name__ == '__main__':
	print "create testfolder on /drone/dronekit-sitl/picture/testfolder"
	making_direc("drone/dronekit-sitl/picture/","testfolder")
	print "test create success , start transfer to 120.126.145.102..."
	transfer("/drone/dronekit-sitl/picture/","testfolder")
	print "remote transfer complete..."
