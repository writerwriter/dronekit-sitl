import time
import picamera
def pi_camera_capture(camera):
    camera.capture("../picture/"+time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())+".png")
    time.sleep(1)
def pi_camera_recording(camera):
<<<<<<< HEAD
	camera.start_recording(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())+".h264")
=======
	camera.start_recording("time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())+".h264")
>>>>>>> 6edb4b5da80281f7106a1348ad04e0b0db48fbba
def pi_camera_resolution(camera, length, width):
	camera.resolution = (length, width)
if __name__ == '__main__':
	
	choice = raw_input('1.photo 2.recording : ')
	camera = picamera.PiCamera()
<<<<<<< HEAD
	print "choice is %d" % int(choice)
	if int(choice) == 1:
		print "test capture"
		camera.capture('./cameratest/test_pi.jpg')
	elif int(chlice) == 2:
		print "get camera object"
		pi_camera_resolution(camera,640,480)
		print "change resolution to 640x480"
		camera.start_recording(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())+".h264")
		print "start recording for 10 seconds"
		camera.wait_recording(10)
		camera.stop_recording()
		print "finish recording"
=======
	pi_camera_resolution(camera, 1920, 1080)
	camera.resolution = (1920, 1080)
	pi_camera_capture(camera)
>>>>>>> 6edb4b5da80281f7106a1348ad04e0b0db48fbba
