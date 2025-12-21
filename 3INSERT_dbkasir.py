#membuat database
import mysql.connector

conn=mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    database='pythondasar',
    password= '',
)

mycursor=conn.cursor()
query= "INSERT INTO produk(name_product, expired_date, price) VALUES(%s,%s,%s)"
value= ("GUNUNG 600ML", 12122027, 3000)

mycursor.execute(query,value)
conn.commit()
print("{}data berhasil dimasukkan".format(mycursor.rowcount))
conn.close()