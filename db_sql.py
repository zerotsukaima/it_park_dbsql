import sqlite3

conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()

cursor.execute(''' CREATE TABLE users
                   (id INT PRIMARY KEY   NOT NULL,
                   user           TEXT   NOT NULL,
                   password       TEXT   NOT NULL); ''')

cursor.execute(''' CREATE TABLE tables
                   (id INT PRIMARY KEY   NOT NULL,
                   name_tab       TEXT   NOT NULL,
                   owner          TEXT   NOT NULL,
                   users          TEXT); ''')

cursor.close()

