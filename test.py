import MySQLdb

db = MySQLdb.connect(host="120.126.145.102",user="drone",passwd="dronemysql",db="106project")

missionid = 48
pointnum = 2
image_str = "image/test/123"
txt_str = "test_string"

cursor = db.cursor()

cursor.execute("INSERT iNTO image_display(mission_id, pointNum,image, txt) VALUES (%s,%s,%s,%s)",(missionid,pointnum,image_str,txt_str))
cursor.close()
db.commit()