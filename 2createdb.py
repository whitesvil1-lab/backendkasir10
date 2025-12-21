#membuat database
import mysql.connector

conn=mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    database='pythondasar',
    password= ''
)

myconn=conn.cursor()
myconn.execute("CREATE DATABASE pythondasar")

print("nama database berhasil dibuat")