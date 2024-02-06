import sqlite3
from datetime import datetime

conn = sqlite3.connect("OutfitGenieInfo.db")
c = conn.cursor()
#
# statement = """ALTER TABLE Clothing_Items
#             ADD Date_Created datetime;"""
# c.execute(statement)

now = datetime.now()
now_str = now.strftime("%Y-%m-%d %H:%M:%S")
print(now_str)
statement = """UPDATE Clothing_Items
                SET Date_Created = ?
                WHERE Item_ID = 'BBC0001';"""
c.execute(statement, (now_str,))

conn.commit()
conn.close()
