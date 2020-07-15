import numpy as np
import sqlite3
import os

try:
    os.remove("albion.db")
    sqliteConnection = sqlite3.connect("albion.db")
    cursor = sqliteConnection.cursor()
    cursor.execute('''PRAGMA foreign_keys = 1''')
    print("Database created and Successfully Connected to SQLite")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Item_Type
        (
            name TINYTEXT NOT NULL UNIQUE
        );
    ''')

    cursor.execute("INSERT INTO Item_Type (name) VALUES ('Hide');")
    cursor.execute("INSERT INTO Item_Type (name) VALUES ('Leather');")
    cursor.execute("INSERT INTO Item_Type (name) VALUES ('Ore');")
    cursor.execute("INSERT INTO Item_Type (name) VALUES ('Ingot');")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Item
        (
            name TINYTEXT NOT NULL UNIQUE,
            type TINYTEXT NOT NULL,
            tier TINYINT NOT NULL,
            FOREIGN KEY (type) REFERENCES Item_Type(name) ON UPDATE CASCADE ON DELETE NO ACTION
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS has_ingredient
        (
            crafted_item_id TINYINT NOT NULL,
            ingredient_item_id TINYINT NOT NULL,
            ingredient_item_quantity TINYINT NOT NULL,
            PRIMARY KEY (crafted_item_id, ingredient_item_id),
            FOREIGN KEY (crafted_item_id) REFERENCES Item(rowid) ON UPDATE CASCADE ON DELETE NO ACTION,
            FOREIGN KEY (ingredient_item_id) REFERENCES Item(rowid) ON UPDATE CASCADE ON DELETE NO ACTION
        );
    ''')

    def insert_item(item_name, item_type, item_tier):
        cursor.execute(
            "INSERT INTO item (name,type,tier)" +
            " VALUES ('" + item_name + "','" + item_type + "'," + str(item_tier) + ");"
        )

    def insert_recipe(crafted_item_id, ingredient_item_id, ingredient_item_quantity):
        cursor.execute(
            "INSERT INTO has_ingredient (crafted_item_id, ingredient_item_id, ingredient_item_quantity)" +
            " VALUES (" + crafted_item_id + ", " + ingredient_item_id + ", " + ingredient_item_quantity + ");"
        )

    insert_item("Rugged Hide", "Hide", 2)

    sqliteConnection.commit()

    return_rate = 0.367
    item_number = 141

    total_crafted = 0
    remaining = item_number

    while remaining != 0:
        total_crafted += remaining
        remaining = np.floor(return_rate * remaining)
        print(str(total_crafted) + " " + str(remaining))

    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("The SQLite connection is closed")
