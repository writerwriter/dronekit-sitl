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
	sql = "SELECT MAX(mission_id) FROM mission_results"
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
	sql = "SELECT MAX(mission_id) FROM mission_option"
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
	sql = "SELECT * FROM mission_option WHERE mission_id > %d" % Id
	cursor = getCursor(db)
	try:
		cursor.execute(sql)
		results  = cursor.fetchall()
		cursor.close()
		last_mission_id = findResultMaxId(db)
		print "Task to do:"
		for record in results:
			if last_mission_id != record[7]:
				print "mission %s:" % record[7]
				last_mission_id = record[7]
			isData = 1
			col1 =record[0]
			col2 =record[1]
			col3 =record[2]
			missionid = record[7]
			print "		point_id : %s Latitude : %s Longitude : %s" % (col1,col2,col3)
		if(isData == 0):
			print "No Task to Do !"
	except :
		db.rollback()
def getNextMission(db,Id = None):
	next_mission = None
	if(Id is None):
		Id = 0
	sql = "SELECT * FROM mission_option WHERE _id = %s" % str(int(Id)+1)
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
			print "Mission : %s Latitude : %s Longitude : %s" % (col1,col2,col3)
	except :
		db.rollback()
	return next_mission
def TaskDone(db,mission,is_abandoned):
	sql = "INSERT iNTO mission_results(mission_id, mission_latitude, mission_longitude,pm25,complete_id,is_abandoned) VALUES (%d,%.15f,%.15f,%d,%d,%i)" % (mission.mission_id,mission.mission_latitude,mission.mission_longitude,mission.pm25,mission.mission_id+1,is_abandoned)
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
			check = raw_input("you want to fly?(Y/n)")
			if check is 'Y':
				next_mission = getNextMission(db,next_mission.mission_id)
				print "doing things"
				next_mission.setPM25(random.randint(1,100))
				TaskDone(db,next_mission,False)
			elif check is 'n':
				next_mission = getNextMission(db,next_mission.mission_id)
				TaskDone(db,next_mission,True)
			print "Last Task is %s" % findResultMaxId(db)
	print ""
	print "All Task Done !"
	closeDatabase(db)
