class Mission:
	def __init__(self, waypoint_id, mission_latitude, mission_longitude, photo_sensor, video_sensor, pm25_sensor, mission_id):
		self.waypoint_id = waypoint_id
		self.mission_latitude = mission_latitude
		self.mission_longitude = mission_longitude
		self.photo_sensor = photo_sensor
		self.video_sensor = video_sensor
		self.pm25_sensor = pm25_sensor
		self.mission_id = mission_id
	def set_pm25_data(self, pm25):
		self.pm25_data = pm25
	def set_point_num(self,point):
		self.point_num = point