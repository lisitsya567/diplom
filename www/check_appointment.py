import pymysql

conn = pymysql.connect(host='localhost', user='root', password='A02032178a', database='medetsinaplus')

cursor = conn.cursor()

cursor.execute("DESCRIBE appointment")

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()

conn.close() 






























