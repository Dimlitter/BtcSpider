import pymysql
mydb = pymysql.connect(
  host="52.140.201.211",       
  user="e5sub",    
  passwd="ZGkTzxhLL8HLknPF" 
)

mycursor = mydb.cursor()
mycursor.execute("use e5sub")

mycursor.execute("select id from users where alias regexp '^vi'")
r = mycursor.fetchall()
print(r)

for record in r :
    print(record)
mydb.close