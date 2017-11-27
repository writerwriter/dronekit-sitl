import time
import picamera
camera = picamera.PiCamera()
camera.capture("../picture/test.png")
time.sleep(1)

