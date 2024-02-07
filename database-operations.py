import sqlite3
from datetime import datetime

conn = sqlite3.connect("OutfitGenieInfo.db")
c = conn.cursor()
#
# statement = """ALTER TABLE Clothing_Items
#             ADD Date_Created datetime;"""
# c.execute(statement)

# statement = """CREATE TABLE Occasions_Suitable_Colours (
#                 Occasion_ID text NOT NULL,
#                 Suitable_Colour text NOT NULL,
#                 FOREIGN KEY (Occasion_ID) REFERENCES Occasions(Occasion_ID),
#                 PRIMARY KEY (Occasion_ID, Suitable_Colour));"""
# c.execute(statement)


# # Create a new table with the foreign key constraint
# c.execute("""CREATE TABLE Outfit_Items(
#             Outfit_ID text NOT NULL,
#             Item_ID text NOT NULL,
#             FOREIGN KEY (Outfit_ID) REFERENCES User_Outfits(Outfit_ID),
#             FOREIGN KEY (Item_ID) REFERENCES Clothing_Items(Item_ID),
#             PRIMARY KEY (Outfit_ID, Item_ID)
#             );""")
#
# # Copy the data from the old table to the new table
# c.execute("INSERT INTO Outfit_Clothing SELECT * FROM Outfit_Items;")
#
# # Drop the old table
# c.execute("DROP TABLE Outfit_Items;")
#
# c.execute("ALTER TABLE Outfit_Clothing RENAME TO Outfit_Items;")

statement = """CREATE TABLE Colour_Combinations(
                Primary_Colour text NOT NULL,
                Comp_Colour text NOT NULL
                """

conn.commit()
conn.close()
