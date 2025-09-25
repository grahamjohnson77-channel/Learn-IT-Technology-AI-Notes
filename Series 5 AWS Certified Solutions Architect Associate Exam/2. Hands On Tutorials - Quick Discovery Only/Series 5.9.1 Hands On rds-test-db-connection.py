import pymysql

db = pymysql.connect(host="rds-mysql-10mintutorial.cfuuua04mrq3.us-east-1.rds.amazonaws.com",port=3306,user="masterUsername",passwd="masterUsername")
cursor=db.cursor()
cursor.execute("SHOW DATABASES")
results=cursor.fetchall()
for result in results:
    print (result)