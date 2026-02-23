"""Database management for Lost and Found application."""

import sqlite3
from typing import List

from src.models.item import Item


class DatabaseManager:
    """
    Handles all SQLite3 database operations for the application.
    
    Attributes:
        db_name (str): The name/path of the SQLite database file.
    """
    def __init__(self, db_name: str = "lost_and_found.db") -> None:
        self.db_name = db_name
        self._initialize_db()
        
    def _initialize_db(self) -> None:
        """Creates the items table if it does not already exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL,
                    location TEXT NOT NULL,
                    status TEXT NOT NULL,
                    contact_info TEXT NOT NULL
                )
                """
            )
    
    def add_item(self, item: Item) -> int:
        """
        Adds a new item to the database.
        
        Args:
            item (Item): The validated Item object to store.
            
        Returns:
            int: The generated database ID of the newly inserted item.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO items (name, category, date, location, status, contact_info) 
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    item.name,
                    item.category,
                    item.date,
                    item.location,
                    item.status,
                    item.contact_info
                )
            )
            new_id = cursor.lastrowid
            item.id = new_id
            return new_id if new_id else 0
        return 0
    
    def get_all_items(self) -> List[Item]:
        """
        Retrieves all items from teh database.

        Returns:
            List[Item]: A list of Item objects representing every row in the DB.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, category, date, location, status, contact_info FROM items"
            )
            rows = cursor.fetchall()
            
            items = []
            for row in rows:
                item = Item(
                    id=row[0],
                    name=row[1],
                    category=row[2],
                    date=row[3],
                    location=row[4],
                    status=row[5],
                    contact_info=row[6]
                )
                items.append(item)
        return items
    
    def update_item(self, item: Item) -> bool:
        """
        Updates an existing item in the database.
        
        Args:
            item (Item): The Item object containing updated data.
            
        Returns:
            bool: True if the update was successful, False if the ID was not found.
        """
        if item.id is None:
            return False
        
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE items
                SET name = ?, category = ?, date = ?, location = ?, status = ?, contact_info = ?
                WHERE id = ?
                """,
                (
                    item.name,
                    item.category,
                    item.date,
                    item.location,
                    item.status,
                    item.contact_info,
                    item.id
                )
            )
            return cursor.rowcount > 0
    
    def delete_item(self, item_id: int) -> bool:
        """
        Deletes an item from the database by its ID.
        
        Args:
            item_id (int): The database ID of the item to remove.
            
        Returns:
            bool: True if the deletion was successful, False if the ID was not found.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM items WHERE id = ?", 
                (item_id,)
            )
            return cursor.rowcount > 0