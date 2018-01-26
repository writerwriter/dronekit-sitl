import MySQLdb
import Mission
import random
import time


def getCursor(db):
	cursor = db.cursor()
	return cursor
def closeDatabase(db):
	db.close()
def findResultMaxId(db):
	maxId = -1
	sql = "SELECT MAX(waypoint_id) FROM mission_results"
	cursor = getCursor(db)
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		cursor.close()
		for record in results:
			maxId = record[0]
	except:
		db.rollback()
	return maxId
def findMissionMaxId(db):
	maxId = -1
	sql = "SELECT MAX(waypoint_id) FROM mission_option"
	cursor = getCursor(db)
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		cursor.close()
		for record in results:
			maxId = record[0]
	except:
		db.rollback()
	return maxId
def printTask(db,Id = None):
	if(Id is None):
		Id = 0
	isData = 0
	sql = "SELECT * FROM mission_option WHERE waypoint_id > %d" % Id
	cursor = getCursor(db)
	try:
		cursor.execute(sql)
		results  = cursor.fetchall()
		cursor.close()
		last_mission_id = findResultMaxId(db)
		print "Task to do:"
		for record in results:
			isData = 1
			col1 =record[0]
			col2 =record[1]
			col3 =record[2]
			photo_s = record[4]
			video_s = record[5]
			pm25_s = record[6]
			print "	point_id : %s Latitude : %s Longitude : %s Photo:%s Video:%s Pm25:%s" % (col1,col2,col3,photo_s,video_s,pm25_s)
		if(isData == 0):
			print "No Task to Do !"
	except :
		db.rollback()
def getNextMission(db,Id = None):
	next_mission = None
	if(Id is None):
		Id = 0
	sql = "SELECT * FROM mission_option WHERE waypoint_id = %s" % str(int(Id)+1)
	cursor = getCursor(db)
	try:
		cursor.execute(sql)
		results  = cursor.fetchall()
		cursor.close()
		for record in results:
			next_mission = Mission.Mission(record[0],record[1],record[2],record[4],record[5],record[6])
			col1 =record[0]
			col2 =record[1]
			col3 =record[2]
			photo_s = record[4]
			video_s = record[5]
			pm25_s = record[6]
			print "	point_id : %s Latitude : %s Longitude : %s Photo:%s Video:%s Pm25:%s" % (col1,col2,col3,photo_s,video_s,pm25_s)
	except :
		db.rollback()
	return next_mission
def TaskDone(db,mission,is_abandoned):
	sql = "INSERT iNTO mission_results(waypoint_id, mission_latitude, mission_longitude,pm25,is_abandoned) VALUES (%d,%.15f,%.15f,%d,%i)" % (mission.mission_id,mission.mission_latitude,mission.mission_longitude,mission.pm25,is_abandoned)
	cursor = getCursor(db)
	try:
		cursor.execute(sql)
		cursor.close()
		db.commit()
		if is_abandoned == False:
			print "mission %d complete." % mission.mission_id
		else:
			print "Mission %d has been abandoned." % mission.mission_id
	except:
		db.rollback()
if __name__ == '__main__':
	db = MySQLdb.connect(host="120.126.145.102",user="drone",passwd="dronemysql",db="106project")
	Id = findResultMaxId(db)
	print "Last Task is %s" % Id
	next_mission = getNextMission(db,str(int(Id)-1)) #fianl mission
	while True:
		closeDatabase(db)
		db = MySQLdb.connect(host="120.126.145.102",user="drone",passwd="dronemysql",db="106project")
		if findResultMaxId(db) < findMissionMaxId(db):
			printTask(db,findResultMaxId(db))
			#doing mission
			
			#check = raw_input("you want to fly?(Y/n)")
			check = "Y"
			if check is 'Y':
				next_mission = getNextMission(db,next_mission.mission_id)
				ispm25 = int(next_mission.pm25_sensor)
				print next_mission.pm25_sensor,next_mission.video_sensor,next_mission.photo_sensor
				print "doing things"
				if(ispm25==1):
					next_mission.setPM25(random.randint(1,100))
				TaskDone(db,next_mission,False)
			elif check is 'n':
				next_mission = getNextMission(db,next_mission.mission_id)
				TaskDone(db,next_mission,True)
			print "Last Task is %s" % findResultMaxId(db)
	print ""
	print "All Task Done !"
	closeDatabase(db)