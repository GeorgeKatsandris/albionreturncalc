import sqlite3
import os.path
from typing import List, Tuple


def db_init():
    if os.path.exists("albion.db"):
        os.remove("albion.db")

    try:
        sqlite_connection = sqlite3.connect("albion.db")
        cursor = sqlite_connection.cursor()
        cursor.execute('''PRAGMA foreign_keys = 1''')

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Item_Type
            (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TINYTEXT NOT NULL UNIQUE
            );
        """)

        def insert_type(item_type: str) -> None:
            cursor.execute("INSERT INTO Item_Type (name) VALUES ('" + item_type + "');")

        insert_type("Hide")
        insert_type("Leather")
        insert_type("Ore")
        insert_type("Ingot")
        print("Added Item_Type table")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Recipe
            (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                crafted_item_id INT NOT NULL,
                FOREIGN KEY (crafted_item_id) REFERENCES Item(id) ON UPDATE CASCADE ON DELETE NO ACTION
            );
        """)
        print("Added Recipe table")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Item
            (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TINYTEXT NOT NULL UNIQUE,
                type TINYTEXT NOT NULL,
                tier TINYINT NOT NULL,
                FOREIGN KEY (type) REFERENCES Item_Type(name) ON UPDATE CASCADE ON DELETE NO ACTION
            );
        """)

        def insert_item(item_name: str, item_type: str, item_tier: int) -> None:
            cursor.execute(
                "INSERT INTO item (name,type,tier)" +
                " VALUES ('" + item_name + "','" + item_type + "'," + str(item_tier) + ");"
            )

        insert_item("Rugged Hide", "Hide", 2)
        insert_item("Stiff Leather", "Leather", 2)
        print("Added Item table")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS has_ingredient
            (
                recipe_id INT NOT NULL,
                ingredient_item_id INT NOT NULL,
                ingredient_item_quantity TINYINT NOT NULL,
                PRIMARY KEY (recipe_id, ingredient_item_id),
                FOREIGN KEY (recipe_id) REFERENCES Recipe(id) ON UPDATE CASCADE ON DELETE NO ACTION,
                FOREIGN KEY (ingredient_item_id) REFERENCES Item(id) ON UPDATE CASCADE ON DELETE NO ACTION
            );
        """)

        def insert_recipe(crafted_item_name: str, ingredients: List[Tuple[str, int]]) -> None:
            cursor.execute("SELECT id FROM Item WHERE name == '" + crafted_item_name + "';")
            crafted_item_id = cursor.fetchone()[0]

            cursor.execute("INSERT INTO Recipe (crafted_item_id) VALUES (" + str(crafted_item_id) + ");")
            recipe_id = cursor.lastrowid

            for ingredient in ingredients:
                ingredient_item_name = ingredient[0]
                ingredient_item_quantity = ingredient[1]

                cursor.execute("SELECT id FROM Item WHERE name == '" + ingredient_item_name + "';")
                ingredient_item_id = cursor.fetchone()[0]

                cursor.execute(
                    "INSERT INTO has_ingredient (recipe_id, ingredient_item_id, ingredient_item_quantity)" +
                    " VALUES (" +
                    str(recipe_id) + ", " +
                    str(ingredient_item_id) + ", " +
                    str(ingredient_item_quantity) + ");")

        insert_recipe("Stiff Leather", [("Rugged Hide", 1)])
        print("Added has_ingredient table")

        sqlite_connection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


db_init()
