import sqlite3

conn = sqlite3.connect("user_information.db")
c = conn.cursor()
# c.execute("""CREATE TABLE logins (
#             user_id INTEGER PRIMARY KEY,
#             username TEXT NOT NULL,
#             password TEXT NOT NULL
#             )""")
# c.execute("""CREATE TABLE clothingItems (
#             item_id INTEGER PRIMARY KEY,
#             user_id INTEGER,
#             clothing_type TEXT,
#             primary_colour TEXT,
#             fit TEXT,
#             warmth TEXT,
#             occasions TEXT,
#             image BLOB,
#             FOREIGN KEY (user_id) REFERENCES logins(user_id)
#             )
#             """)
# c.execute("""CREATE TABLE Occasions (
#             occasion_id INTEGER PRIMARY KEY,
#             name TEXT
#             )""")

# c.execute("""CREATE TABLE outfits (
#             outfit_id INTEGER PRIMARY KEY,
#             user_id INTEGER,
#             clothingItems TEXT,
#             occasions TEXT,
#             FOREIGN KEY (user_id) REFERENCES logins(user_id)
#             )
#             """)
# def convert_binary_data(filename):
#     with open (filename, "rb") as file:
#         blobData = file.read()
#     return blobData
# occasions = [7,8]
# blob = convert_binary_data("C:/Users/jasmi/Downloads/tshirt.png")
#
# c.execute(""" INSERT INTO clothingItems (item_id, user_id, clothing_type, primary_colour, fit, warmth, occasions, image)
#             VALUES (0, "0", "t-shirt","white", "baggy", "cold", ?, ?)""", ( ','.join(map(str, occasions)), blob))


c.execute("""INSERT INTO Occasions (occasion_id, name) VALUES
            (2, "Formal Party"),
            (3, "Wedding"),
            (4, "Festive/Holiday Party"),
            (5, "Casual Wedding"),
            (6, "Baby Shower"),
            (7, "Family Event"),
            (8, "Cruise"),
            (9, "Job Interview"),
            (10, "Work Function"),
            (11, "Friend Meetup")""")

conn.commit()
conn.close()