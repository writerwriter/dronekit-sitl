class Mission:
	def __init__(self, mission_id, mission_latitude, mission_longitude, photo_sensor, video_sensor, pm25_sensor, pm25 = 0):
		self.mission_id = mission_id
		self.mission_latitude = mission_latitude
		self.mission_longitude = mission_longitude
		self.photo_sensor = photo_sensor
		self.video_sensor = video_sensor
		self.pm25_sensor = pm25_sensor
		self.pm25 = pm25

	def setPM25(self,pm25):
		self.pm25 = pm25