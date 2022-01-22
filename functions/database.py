import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	username="root",
	password="",
	database="productreserver"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM user")

print(mycursor)
for x in mycursor:
  print(x)