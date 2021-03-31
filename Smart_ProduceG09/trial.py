order_id = 1
import sqlite3

conn = sqlite3.connect('db.sqlite3')
tuple1 = (order_id, )
query = ''' SELECT status from accounts_order where id == ? '''

cursor = conn.execute(query, tuple1)
print(cursor.fetchall())
context = {}
