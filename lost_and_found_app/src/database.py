import sqlite3
from typing import List
from src.models import Item, ItemStatus


class InventoryManager:
    """
    Manages the inventory of the lost and found items in a SQLite database.
    """
    
    def __init__(self, db_name: str = "lost_and_found.db") -> None:
        """
        Initializes the databse manager and opens the connection.

        Args:
            db_name (str, optional): The filename for the database. Defaults to "lost_and_found.db".
                                     Use ':memory:' for temporary in-memory database testing.
        """
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
    
    def initialize_db(self) -> None:
        """
        Creates the table required for the database, if it does not exist.
        """
        query = """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                date_lost TEXT NOT NULL,
                location TEXT NOT NULL,
                status TEXT NOT NULL,
                contact_info TEXT NOT NULL
            )
        """
        with self.conn:
            self.conn.execute(query)
    
    def close(self) -> None:
        """
        Closes the active database connection, if it exists.
        """
        if self.conn:
            self.conn.close()
    
    def add_item(self, item: Item) -> int:
        """
        Adds a new item to the database.
        
        Args:
            item (Item): The item object to add to the database.
            
        Returns:
            int: the ID of the newly inserted row.
        """
        query = """
            INSERT INTO items (name, category, date_lost, location, status, contact_info)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        with self.conn:
            cursor = self.conn.execute(query, (
                item.name,
                item.category,
                item.date_lost,
                item.location,
                item.status.value,
                item.contact_info
            ))
            cursor_id = cursor.lastrowid
            return cursor_id if cursor_id else -1
    
    def update_item_status(self, item_id: int, new_status: ItemStatus) -> None:
        """
        Updates the status of a specified item.

        Args:
            item_id (int): The ID of the item to update.
            new_status (ItemStatus): The new status of the item to set.
        """
        query = "UPDATE items SET status = ? WHERE id = ?"
        with self.conn:
            self.conn.execute(query, (new_status.value, item_id))
    
    def delete_item(self, item_id: int) -> None:
        """
        Deletes a specified item from the database.

        Args:
            item_id (int): The ID of the item to be deleted.
        """
        query = "DELETE FROM items WHERE id = ?"
        with self.conn:
            self.conn.execute(query, (item_id,))
    
    def get_all_items(self) -> List[Item]:
        """
        Retrieves all items current in the database.

        Returns:
            List[Item]: A list of all Item objects in database.
        """
        query = "SELECT * FROM items"
        cursor = self.conn.execute(query)
        rows = cursor.fetchall()
        return [self._row_to_item(row) for row in rows]
    
    def search_items(self, keyword: str) -> List[Item]:
        """
        Searches for items by name, location or category using a keyword.

        Args:
            keyword (str): The search term.

        Returns:
            List[Item]: A list of matching Item objects.
        """
        query = """
            SELECT * FROM items
            WHERE name LIKE ? OR location LIKE ? OR category LIKE ?
        """
        search_term = f"%{keyword}"
        cursor = self.conn.execute(query, (search_term, search_term, search_term))
        rows = cursor.fetchall()
        return [self._row_to_item(row) for row in rows]
    
    def filter_by_status(self, status: ItemStatus) -> List[Item]:
        """
        Filters items by their current status.

        Args:
            status (ItemStatus): The status to filter by.

        Returns:
            List[Item]: A list of matching Item objects.
        """
        query = "SELECT * FROM items WHERE status = ?"
        cursor = self.conn.execute(query, (status.value,))
        rows = cursor.fetchall()
        return [self._row_to_item(row) for row in rows]
    
    def _row_to_item(self, row: tuple) -> Item:
        """
        Helper method to convert a database row to an Item object.

        Args:
            row (tuple): The row information tuple returned from the database.

        Returns:
            Item: An Item object containing the row information.
        """
        return Item(item_id=row[0],
                    name=row[1],
                    category=row[2],
                    date_lost=row[3],
                    location=row[4],
                    status=ItemStatus(row[5]),
                    contact_info=row[6])
        