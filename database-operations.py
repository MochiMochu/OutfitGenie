import sqlite3
from sqlite3 import Error
from datetime import datetime
import uuid

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

# # creates the table for listing colour combinations (i.e. two colours that go well together)
# def create_colour_combos(connection):
#     c = connection.cursor()
#     statement = """CREATE TABLE Colour_Combos (
#                     Primary_Colour text NOT NULL,
#                     Matching_Colour text NOT NULL,
#                     PRIMARY KEY (Primary_Colour, Matching_Colour)
#                     );"""
#     try:
#         c.execute(statement)
#     except Error as e:
#         print(e)
#     finally:
#         connection.commit()
#
#
# # creates the table for listing colours that are appropriate for certain occasions
# def create_occasion_colours(connection):
#     c = connection.cursor()
#     statement = """CREATE TABLE Occasion_Colours(
#                     Occasion_ID text NOT NULL,
#                     Appropriate_Colour text NOT NULL,
#                     FOREIGN KEY (Occasion_ID) REFERENCES Occasions(Occasion_ID),
#                     PRIMARY KEY (Occasion_ID, Appropriate_Colour)
#                     );"""
#     try:
#         c.execute(statement)
#     except Error as e:
#         print(e)
#     finally:
#         connection.commit()
#
#
# # populates the colour combination table with predefined pairings of complimentary colours
# def populate_colour_combos(connection):
#     c = connection.cursor()
#     pink_pairings = [("pink", "light blue"), ("pink", "dark blue"), ("pink", "grey"), ("pink", "white"), ("pink", "black"), ("pink", "beige"), ("pink", "red"), ("pink", "denim")]
#     c.executemany("INSERT INTO Colour_Combos VALUES (?, ?)", pink_pairings)
#
#     red_pairings = [("red", "light blue"), ("red", "dark blue"), ("red", "grey"), ("red", "white"), ("red", "black"), ("red", "pink"), ("red", "beige"), ("red", "denim")]
#     c.executemany("INSERT INTO Colour_Combos VALUES (?, ?)", red_pairings)
#
#     orange_pairings = [("orange", "green"), ("orange", "light blue"), ("orange", "dark blue"), ("orange", "white"), ("orange", "black"), ("orange", "beige"), ("orange", "brown"), ("orange", "denim")]
#     c.executemany("INSERT INTO Colour_Combos VALUES (?, ?)", orange_pairings)
#
#     beige_pairings = [("beige", "navy"), ("beige", "purple"), ("beige", "brown"), ("beige", "white"), ("beige", "black"), ("beige", "yellow"), ("beige", "orange"), ("beige", "red"), ("beige", "pink"), ("beige", "denim")]
#     c.executemany("INSERT INTO Colour_Combos VALUES (?, ?)", beige_pairings)
#
#     yellow_pairings = [("yellow", "green"), ("yellow", "dark blue"), ("yellow", "white"), ("yellow", "black"), ("yellow", "beige"), ("yellow", "denim")]
#     c.executemany("INSERT INTO Colour_Combos VALUES (?, ?)", yellow_pairings)
#
#     green_pairings = [("green", "orange"), ("green", "purple"), ("green", "white"), ("green", "black"), ("green", "yellow"), ("green", "light blue"), ("green", "denim")]
#     c.executemany("INSERT INTO Colour_Combos VALUES (?, ?)", green_pairings)
#
#     lightblue_pairings = [("light blue", "pink"), ("light blue", "red"), ("light blue", "orange"), ("light blue", "white"), ("light blue", "black"),
#                           ("light blue", "dark blue"), ("light blue", "purple"), ("light blue", "denim")]
#     c.executemany("INSERT INTO Colour_Combos VALUES (?, ?)", lightblue_pairings)
#
#     darkblue_pairings = [("dark blue", "pink"), ("dark blue", "red"), ("dark blue", "yellow"), ("dark blue", "grey"), ("dark blue", "white"), ("dark blue", "black"),
#                          ("dark blue", "light blue"), ("dark blue", "purple"), ("dark blue", "denim")]
#     c.executemany("INSERT INTO Colour_Combos VALUES (?, ?)", darkblue_pairings)
#
#     purple_pairings = [("purple", "orange"), ("purple", "grey"), ("purple", "green"), ("purple", "white"), ("purple", "black"), ("purple", "light blue"), ("purple", "dark blue"), ("purple", "denim")]
#     c.executemany("INSERT INTO Colour_Combos VALUES (?, ?)", purple_pairings)
#
#     brown_pairings = [("brown", "beige"), ("brown", "white"), ("brown", "black"), ("brown", "orange"), ("brown", "denim")]
#     c.executemany("INSERT INTO Colour_Combos VALUES (?, ?)", brown_pairings)
#
#     grey_pairings = [("grey", "pink"), ("grey", "red"), ("grey", "dark blue"), ("grey", "purple"), ("grey", "white"), ("grey", "black"), ("grey", "denim")]
#     c.executemany("INSERT INTO Colour_Combos VALUES (?, ?)", grey_pairings)
#
#     navy_pairings = [("navy", "pink"), ("navy", "red"), ("navy", "yellow"), ("navy", "grey"), ("navy", "white"), ("navy", "black"), ("navy", "light blue"), ("navy", "purple"), ("navy", "denim")]
#     c.executemany("INSERT INTO Colour_Combos VALUES (?, ?)", navy_pairings)
#
#     lightgreen_pairings = [("light green", "white"), ("light green", "brown"), ("light green", "orange"), ("light green", "purple"), ("light green", "pink"), ("light green", "navy"), ("light green", "black"), ("light green", "denim")]
#     c.executemany("INSERT INTO Colour_Combos VALUES (?, ?)", lightgreen_pairings)
#
#     khaki_pairings = [("khaki", "white"), ("khaki", "denim"), ("khaki", "black"), ("khaki", "grey"), ("khaki", "navy"), ("khaki", "dark blue"), ("khaki", "brown"), ("khaki", "pink")]
#     c.executemany("INSERT INTO Colour_Combos VALUES (?, ?)", khaki_pairings)
#
#     black_pairings = [("black", "black"), ("black", "red"), ("black", "green"), ("black", "light green"), ("black", "purple"), ("black", "yellow"), ("black", "orange"),
#                       ("black", "pink"), ("black", "white"), ("black", "brown"), ("black", "grey"), ("black", "beige"), ("black", "navy"), ("black", "khaki"), ("black", "denim"),
#                       ("black", "light blue"), ("black", "dark blue")]
#     c.executemany("INSERT INTO Colour_Combos VALUES (?, ?)", black_pairings)
#
#     white_pairings = [("white", "black"), ("white", "red"), ("white", "green"), ("white", "light green"), ("white", "purple"), ("white", "yellow"), ("white", "orange"),
#                       ("white", "pink"), ("white", "white"), ("white", "brown"), ("white", "grey"), ("white", "beige"), ("white", "navy"), ("white", "khaki"), ("white", "denim"),
#                       ("white", "light blue"), ("white", "dark blue")]
#     c.executemany("INSERT INTO Colour_Combos VALUES (?,?)", white_pairings)
#
#     denim_pairings = [("denim", "black"), ("denim", "red"), ("denim", "green"), ("denim", "light green"), ("denim", "purple"), ("denim", "yellow"), ("denim", "orange"),
#                       ("denim", "pink"), ("denim", "white"), ("denim", "brown"), ("denim", "grey"), ("denim", "beige"), ("denim", "navy"), ("denim", "khaki"), ("denim", "light blue"),
#                       ("denim", "dark blue")]
#     c.executemany("INSERT INTO Colour_Combos VALUES (?,?)", denim_pairings)
#     connection.commit()
#
#
# # # populates the occasion colours table with the colours that are suitable for certain occasions
# def populate_occasion_colours(connection):
#     c = connection.cursor()
#     # friend meetup, family event, festive party, religious event and house party not listed here because any colour is suitable
#     work_function_colours = [("WF", "black"), ("WF", "green"), ("WF", "light green"), ("WF", "purple"), ("WF", "pink"), ("WF", "brown"),
#                              ("WF", "grey"), ("WF", "white"), ("WF", "beige"), ("WF", "navy"), ("WF", "khaki"), ("WF", "light blue"), ("WF", "dark blue")]
#     c.executemany("INSERT INTO Occasion_Colours VALUES (?,?)", work_function_colours)
#
#     job_interview_colours = [("JI", "black"), ("JI", "grey"), ("JI", "navy"), ("JI", "white"), ("JI", "beige"), ("JI", "brown")]
#     c.executemany("INSERT INTO Occasion_Colours VALUES (?,?)", job_interview_colours)
#
#     black_tie_affair_colours = [("BTA", "black")]
#     c.executemany("INSERT INTO Occasion_Colours VALUES (?,?)", black_tie_affair_colours)
#
#     wedding_colours = [("W", "red"), ("W", "green"), ("W", "light green"), ("W", "purple"), ("W", "yellow"), ("W", "orange"),
#                        ("W", "pink"), ("W", "brown"), ("W", "navy"), ("W", "light blue"), ("W", "dark blue")]
#     c.executemany("INSERT INTO Occasion_Colours VALUES (?,?)", wedding_colours)
#
#     funeral_colours = [("F", "black"), ("F", "grey"), ("F", "navy")]
#     c.executemany("INSERT INTO Occasion_Colours VALUES (?,?)", funeral_colours)
#     connection.commit()

# def test_occasion_colours(connection, occasion):
#     c = connection.cursor()
#     statement = """SELECT Primary_Colour, Matching_Colour FROM Colour_Combos
#                     JOIN Occasion_Colours ON Occasion_Colours.Appropriate_Colour = Colour_Combos.Primary_Colour
#                     WHERE Occasion_Colours.Occasion_ID = ?
#                         AND EXISTS (
#                             SELECT 1
#                             FROM Occasion_Colours Occasion_Colours2
#                             WHERE Occasion_Colours2.Occasion_ID = Occasion_Colours.Occasion_ID
#                             AND Occasion_Colours2.Appropriate_Colour = Colour_Combos.Matching_Colour
#                             );"""
#     c.execute(statement, (occasion,))
#     results = c.fetchall()
#     print(results)

def create_clothing_categories(connection):
    c = connection.cursor()
    statement = """CREATE TABLE IF NOT EXISTS Clothing_Categories (
                    Category text NOT NULL,
                    Specific_Type text NOT NULL,
                    FOREIGN KEY (Specific_Type) REFERENCES Clothing_Items(Clothing_Type),
                    PRIMARY KEY (Category, Specific_Type)
                    );"""
    try:
        c.execute(statement)
    except Error as e:
        print(e)
    finally:
        connection.commit()

def populate_clothing_categories(connection):
    c = connection.cursor()
    tops_types = [("Tops", "t shirt"), ("Tops", "graphic tee"), ("Tops", "polo shirt"), ("Tops", "corset"), ("Tops", "off shoulder top"), ("Tops", "bodysuit"), ("Tops", "camisole"),
                       ("Tops", "crop top"), ("Tops", "tube top"), ("Tops", "tank top"), ("Tops", "formal shirt"), ("Tops", "blouse")]
    c.executemany("INSERT INTO Clothing_Categories VALUES (?,?)", tops_types)

    dress_types = [("Dress", "mini dress"), ("Dress", "midi skirt"), ("Dress", "maxi skirt"), ("Dress", "bodycon dress")]
    c.executemany("INSERT INTO Clothing_Categories VALUES (?,?)", dress_types)

    hoodies_types = [("Hoodies & Sweatshirts", "sweatshirt"), ("Hoodies & Sweatshirts", "hoodie")]
    c.executemany("INSERT INTO Clothing_Categories VALUES (?,?)", hoodies_types)

    cardigans_types = [("Cardigans & Jumpers", "turtleneck"), ("Cardigans & Jumpers", "jumper"), ("Cardigans & Jumpers", "cardigan")]
    c.executemany("INSERT INTO Clothing_Categories VALUES (?,?)", cardigans_types)

    jackets_types = [("Jackets & Coats", "jacket"), ("Jackets & Coats", "blazer"), ("Jackets & Coats", "gilet"), ("Jackets & Coats", "fur coat"), ("Jackets & Coats", "puffer coat"),
                     ("Jackets & Coats", "parka"), ("Jackets & Coats", "trench coat")]
    c.executemany("INSERT INTO Clothing_Categories VALUES (?,?)", jackets_types)

    trousers_types = [("Trousers", "joggers"), ("Trousers", "jeans"), ("Trousers", "cargo pants"), ("Trousers", "flares"), ("Trousers", "leggings"), ("Trousers", "slacks"),
                      ("Trousers", "suit pants")]
    c.executemany("INSERT INTO Clothing_Categories VALUES (?,?)", trousers_types)

    skirts_types = [("Skirts", "mini skirt"), ("Skirts", "midi skirt"), ("Skirts", "maxi skirt")]
    c.executemany("INSERT INTO Clothing_Categories VALUES (?,?)", skirts_types)

    shorts_types = [("Shorts", "hot pants"), ("Shorts", "bermuda shorts"), ("Shorts", "shorts")]
    c.executemany("INSERT INTO Clothing_Categories VALUES (?,?)", shorts_types)

    jumpsuits_types = [("Jumpsuits & Overalls", "dungarees"), ("Jumpsuits & Overalls", "jumpsuit"), ("Jumpsuits & Overalls", "overalls")]
    c.executemany("INSERT INTO Clothing_Categories VALUES (?,?)", jumpsuits_types)
    connection.commit()

def create_broader_colours(connection):
    c = connection.cursor()
    statement = """CREATE TABLE IF NOT EXISTS Broader_Colours(
                    General_Colour text NOT NULL,
                    Specific_Colour text NOT NULL,
                    FOREIGN KEY (Specific_Colour) REFERENCES Clothing_Items(Primary_Colour),
                    PRIMARY KEY (General_Colour, Specific_Colour)
                    );"""
    try:
        c.execute(statement)
    except Error as e:
        print(e)
    finally:
        connection.commit()

def populate_broader_colours(connection):
    c = connection.cursor()
    colour_pairings = [("Beige", "beige"), ("Grey", "grey"), ("Brown", "brown"), ("Brown", "khaki"), ("Blue", "navy"), ("Blue", "denim"), ("Blue", "light blue"),
                       ("Blue", "dark blue"), ("Green", "light green"), ("Green", "green"), ("Red", "red"), ("Orange", "orange"), ("Pink", "pink"), ("Yellow", "yellow"),
                       ("Purple", "purple"), ("White", "white")]
    c.executemany("INSERT INTO Broader_Colours VALUES (?,?)", colour_pairings)
    connection.commit()
    connection.close()

def create_broader_occasions(connection):
    c = connection.cursor()
    statement = """CREATE TABLE IF NOT EXISTS Broader_Occasions(
                    General_Occasion text NOT NULL,
                    Specific_Occasion text NOT NULL,
                    FOREIGN KEY (Specific_Occasion) REFERENCES Items_Occasions(Occasion_ID),
                    PRIMARY KEY (General_Occasion, Specific_Occasion)
                    );"""
    try:
        c.execute(statement)
    except Error as e:
        print(e)
    finally:
        connection.commit()
        connection.close()


def populate_broader_occasions(connection):
    c = connection.cursor()
    occasion_pairings = [("Casual", "FM"), ("Casual", "FE"), ("Formal", "BTA"), ("Formal", "RE"), ("Formal", "W"), ("Formal", "F"),
                         ("Office Wear", "WF"), ("Office Wear", "JI"), ("Party", "HP"), ("Party", "FP")]
    try:
        c.executemany("INSERT INTO Broader_Occasions VALUES (?,?)", occasion_pairings)
    except Error as e:
        print(e)
    finally:
        connection.commit()
        connection.close()


def create_clothing_levels(connection):
    c = connection.cursor()
    statement = """CREATE TABLE IF NOT EXISTS Clothing_Levels (
                    Level text NOT NULL,
                    Clothing_Type text NOT NULL,
                    PRIMARY KEY (Level, Clothing_Type)
                    );"""
    try:
        c.execute(statement)
    except Error as e:
        print(e)
    finally:
        connection.commit()
        connection.close()


def populate_clothing_levels(connection):
    c = connection.cursor()
    levels_dictionary = {"t-shirt": "top",
                         "graphic tee": "top",
                         "polo shirt": "top",
                         "corset": "top",
                         "off the shoulder top": "top",
                         "bodysuit": "top",
                         "camisole": "top",
                         "crop top": "top",
                         "tube top": "top",
                         "tank top": "top",
                         "formal shirt": "top",
                         "blouse": "top",
                         "turtleneck": "top",
                         "jumper": "outerwear",
                         "cardigan": "outerwear",
                         "sweatshirt": "outerwear",
                         "hoodie": "outerwear",
                         "joggers": "bottom",
                         "jeans": "bottom",
                         "cargo pants": "bottom",
                         "flares": "bottom",
                         "leggings": "bottom",
                         "slacks": "bottom",
                         "suit pants": "bottom",
                         "hot pants": "bottom",
                         "bermuda shorts": "bottom",
                         "shorts": "bottom",
                         "mini skirt": "bottom",
                         "midi skirt": "bottom",
                         "maxi skirt": "bottom",
                         "mini dress": "onepiece",
                         "midi dress": "onepiece",
                         "maxi dress": "onepiece",
                         "bodycon dress": "onepiece",
                         "dungarees": "onepiece",
                         "jumpsuit": "onepiece",
                         "overalls": "onepiece",
                         "blazer": "outerwear",
                         "gilet": "outerwear",
                         "fur coat": "outerwear",
                         "puffer coat": "outerwear",
                         "jacket": "outerwear",
                         "parka": "outerwear",
                         "trench coat": "outerwear"
                         }
    for key, value in levels_dictionary.items():
        try:
            c.execute("INSERT INTO Clothing_Levels VALUES (?,?)", (value, key))
        except Error as e:
            print(e)
    connection.commit()
    connection.close()

if __name__ == "__main__":
    conn = sqlite3.connect("OutfitGenieInfo.db")
    # create_colour_combos(conn)
    # create_occasion_colours(conn)
    # populate_colour_combos(conn)
    # populate_occasion_colours(conn)
    # occasion = "BTA"
    # test_occasion_colours(conn, occasion)
    # populate_clothing_categories(conn)
    # create_broader_colours(conn)
    # populate_broader_colours(conn)
    # create_broader_occasions(conn)
    # populate_broader_occasions(conn)
    c = conn.cursor()
    c.execute("DELETE FROM Clothing_Items WHERE User_ID = '00229ff1-50cb-4636-a9a7-9ff18a8013de' AND Item_ID = 'LRM0001'")
    conn.commit()
    conn.close()

    # create_clothing_levels(conn)
    # populate_clothing_levels(conn)

    # try:
    #     conn.execute('BEGIN TRANSACTION')
    #
    #     c.execute("DELETE FROM Users")
    #     c.execute("DELETE FROM Clothing_Items")
    #     c.execute("DELETE FROM Clothing_Occasions")
    #
    #     conn.commit()
    # except sqlite3.Error as e:
    #     conn.rollback()  # Rollback on error
    #     raise e
    # finally:
    #     conn.commit()
    #     conn.close()


