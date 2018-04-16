import MySQLdb
import sql
#import camera_control as cc
#import picamera

db = MySQLdb.connect(host="120.126.145.102",user="drone",passwd="dronemysql",db="106project")

#camera = picamera.PiCamera() 
#value = cc.capture(camera,"test","test")
#print "locate at %s \n" % value
missionid = 48
pointnum = 2
image_str = "/test_value"
txt_str = "test_string"

cursor = db.cursor()

sql_str = (missionid,pointnum,image_str,txt_str)
print sql_str
cursor.execute("INSERT iNTO image_display(mission_id, pointNum,image, txt) VALUES (%s,%s,%s,%s)",sql_str)
#cursor.execute(sql_str)
cursor.close()
db.commit()