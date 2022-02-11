from time import time
import pymysql
import datetime
mydb = pymysql.connect(
  host="52.140.201.211",       
  user="push",    
  passwd="GSAMz86MZPyyMA7x" 
)

mycursor = mydb.cursor()
mycursor.execute("use push")
print(mycursor.execute("select * from Sheet1"))
myresult = mycursor.fetchall()
print(myresult)
for row in myresult:
  push_id = row[0]
  name = row[1]
  project = row[2]
  date = row[3]
  remark = row[4]
  id = row[5]
  print(push_id, name, project, date, remark, id)
mydb.close