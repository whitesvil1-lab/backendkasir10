#sekarang kita belajar database

import mysql.connector

conn=mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password= ''
)

if conn.is_connected():
    print("sudah terkoneksi dengan database")