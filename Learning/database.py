import mysql.connector

conn = mysql.connector.connect(host='localhost', user='root', password='', database='productreserver')

mycursor = conn.cursor()

mycursor.execute('SELECT * FROM unfilledorders')

myresult = mycursor.fetchall()

for x in myresult:
  print(x)


# use multi processing