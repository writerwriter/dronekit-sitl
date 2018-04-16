import MySQLdb
import sql
import camera_control as cc
import picamera
import folder_transfer as ft

db = MySQLdb.connect(host="120.126.145.102",user="drone",passwd="dronemysql",db="106project")

camera = picamera.PiCamera() 
value = cc.capture(camera,"11","test")
print "locate at %s \n" % value
missionid = 48
pointnum = 2
image_str = value
txt_str = "test_string"

list_str = []
cursor = db.cursor()
my_sql = (missionid,pointnum,image_str,txt_str)
list_str.append(my_sql)
for sql_str in list_str:
    cursor.execute("INSERT INTO image_display(mission_id,pointNum,image,txt) VALUES (%s,%s,%s,%s)",sql_str)
print "Finish execute sql commands"
cursor.close()
db.commit()
