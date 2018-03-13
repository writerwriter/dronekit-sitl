import picamera
import os
import subprocess as sb


def making_direc(tpath,mission_number):
	sb.call(["mkdir",str(tpath+mission_number)])
	print "making directory success"
def transfer(tpath,tag):

	sb.call(["sshpass","-p","unigrid","scp","-r",tpath+tag,"dmcl@120.126.145.102:/var/www/html/dronePicture"])
	print "transfer finish..."


if __name__ == '__main__':
	
	transfer("/drone/dronekit-sitl/picture/","testfolder","testfile.png")
