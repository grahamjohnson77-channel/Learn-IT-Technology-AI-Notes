# Databases

> [!IMPORTANT]
> PLEASE REMEMBER TO DELETE THE AWS RESOURCES AFTER TUTORIAL IS DONE !!!

> [!NOTE]
> Amazon says: MySQL is the world's most popular open source relational database and Amazon RDS (Relational Database Service) makes it easier to set up, operate, and scale MySQL deployments in the cloud. With Amazon RDS, you can deploy scalable MySQL servers in minutes with cost-efficient and resizable hardware capacity.

> [!IMPORTANT]
> Watch Intros
> https://www.youtube.com/watch?v=GvUaA9cygUk

> AWS IAM Core Concepts (Roles etc.) from Be a Better Dev Youtube Channel: (Please script to their channel and hit the like)
> https://www.youtube.com/watch?v=_ZCTvmaPgao

# Tutorial Link
https://aws.amazon.com/getting-started/hands-on/create-mysql-db/?ref=gsrchandson

# Helpful
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.Connecting.AWSCLI.html

# Helpful to setup python on machine
https://blog.futuresmart.ai/how-to-create-a-mysql-db-on-aws-rds-and-connect-with-python-the-ultimate-step-by-step-guide

# Python script to test connection
> REMEMBER to update your host name to your own new DB name if different!
> Copy the below python script to test file (use .py extension):

import pymysql

db = pymysql.connect(host="rds-mysql-10mintutorial.cfuuua04mrq3.us-east-1.rds.amazonaws.com",port=3306,user="masterUsername",passwd="masterUsername")
cursor=db.cursor()
cursor.execute("SHOW DATABASES")
results=cursor.fetchall()
for result in results:
    print (result)

> And run as: 
> python3 "Series 4.9.1 Hands On rds-test-db-connection.py"

> But best to rename the script to something like test-rds-connnection.py

> [!IMPORTANT]
> NEVER EVER check in username and password details to GitHub ... this is just a demo that has already been destroyed for training purposes only.