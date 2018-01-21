import MySQLdb
import Mission
import random
import time


db = MySQLdb.connect(host="120.126.145.102",user="drone",passwd="dronemysql",db="106project")

def getCursor():
	cursor = db.cursor()
	return cursor
def closeDatabase():
	db.close()
def findResultMaxId():
	maxId = -1
	sql = "SELECT MAX(mission_id) FROM mission_results"
	cursor = getCursor()
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		cursor.close()
		for record in results:
			maxId = record[0]
	except:
		db.rollback()
	return maxId
def findMissionMaxId():
	maxId = -1
	sql = "SELECT MAX(mission_id) FROM mission_option"
	cursor = getCursor()
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		cursor.close()
		for record in results:
			maxId = record[0]
	except:
		db.rollback()
	return maxId
def printTask(Id = None):
	if(Id is None):
		Id = 0
	isData = 0
	sql = "SELECT * FROM mission_option WHERE mission_id >= %d" % Id
	cursor = getCursor()
	try:
		cursor.execute(sql)
		results  = cursor.fetchall()
		cursor.close()
		print "Task to do:"
		for record in results:
			isData = 1
			col1 =record[0]
			col2 =record[1]
			col3 =record[2]
			print "Mission : %s Latitude : %s Longitude : %s" % (col1,col2,col3)
		if(isData == 0):
			print "No Task to Do !"
	except :
		db.rollback()
def getNextMission(Id = None):
	next_mission = None
	if(Id is None):
		Id = 0
	sql = "SELECT * FROM mission_option WHERE mission_id = %s" % str(int(Id)+1)
	cursor = getCursor()
	try:
		cursor.execute(sql)
		results  = cursor.fetchall()
		cursor.close()
		for record in results:
			next_mission = Mission.Mission(record[0],record[1],record[2],record[4],record[5],record[6])
			col1 =record[0]
			col2 =record[1]
			col3 =record[2]
			print "Mission : %s Latitude : %s Longitude : %s" % (col1,col2,col3)
	except :
		db.rollback()
	return next_mission
def TaskDone(mission):
	sql = "INSERT iNTO mission_results(mission_id, mission_latitude, mission_longitude,pm25,complete_id) VALUES (%d,%f,%f,%d,%d)" % (mission.mission_id,mission.mission_latitude,mission.mission_longitude,mission.pm25,mission.mission_id+1)
	cursor = getCursor()
	try:
		cursor.execute(sql)
		cursor.close()
		db.commit()
		print "mission %d complete." % mission.mission_id
	except:
		db.rollback()
if __name__ == '__main__':
	Id = findResultMaxId()
	print "Last Task is %s" % Id
	next_mission = getNextMission(str(int(Id)-1)) #fianl mission
	while True:
		closeDatabase()
		db = MySQLdb.connect(host="120.126.145.102",user="drone",passwd="dronemysql",db="106project")
		if findResultMaxId() < findMissionMaxId():
			next_mission = getNextMission(next_mission.mission_id)
			#doing mission
			next_mission.setPM25(random.randint(1,100))
			TaskDone(next_mission)
			print "Last Task is %s" % findResultMaxId()
	print ""
	print "All Task Done !"
	closeDatabase()
