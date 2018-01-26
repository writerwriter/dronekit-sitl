import time
import picamera
def pi_camera_capture(camera):
    camera.capture("../picture/"+time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())+".png")
    time.sleep(1)
def pi_camera_recording(camera):
	camera.start_recording(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())+".h264")
def pi_camera_resolution(camera, length, width):
	camera.resolution = (length, width)
if __name__ == '__main__':
	camera = picamera.PiCamera()
	print "a"
	pi_camera_resolution(camera,640,480)
	print "b"
	camera.start_recording(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())+".h264")
	print "c"
	camera.wait_recording(10)
	camera.stop_recording()
	print "d"
