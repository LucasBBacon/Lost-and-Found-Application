"""Logic controllers for the Lost and Found Application."""

from typing import List, Optional

from src.models.database import DatabaseManager
from src.models.item import Item


class AppController:
    """
    Orchestrates application logic, bridging the UI and database.
    
    Attributes:
        db (DatabaseManager): The database manager instance.
    """
    
    def __init__(self, db_manager: DatabaseManager) -> None:
        """
        Initializes the AppController

        Args:
            db_manager (DatabaseManager): The database manager instance.
        """
        self.db = db_manager
    
    def add_item(self, item: Item) -> int:
        """
        Adds a new item to the database.

        Args:
            item (Item): The item to add.

        Returns:
            int: The generated database ID.
        """
        return self.db.add_item(item)
    
    def get_all_items(self) -> List[Item]:
        """
        Retrieves all items from the database.

        Returns:
            List[Item]: A list of all stored items.
        """
        return self.db.get_all_items()
    
    def update_item(self, item: Item) -> bool:
        """
        Updates an existing item in the database.

        Args:
            item (Item): The item with updated details.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.db.update_item(item)
    
    def delete_item(self, item_id: int) -> bool:
        """
        Deletes an item from the database by its ID.

        Args:
            item_id (int): The ID of the item to delete.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.db.delete_item(item_id)
    
    def search_items(self, keyword: str) -> List[Item]:
        """
        Searches for items containing the keyword in their name, 
        location, or contact info.
        
        The search is case-insensitive. If an empty string is provided, 
        all items are returned.

        Args:
            keyword (str): The search term.

        Returns:
            List[Item]: Items matching the search criteria.
        """
        all_items = self.get_all_items()
        
        if not keyword.strip():
            return all_items
        
        keyword_lower = keyword.strip().lower()
        
        return [
            item for item in all_items
            if keyword_lower in item.name.lower()
            or keyword_lower in item.location.lower()
            or keyword_lower in item.contact_info.lower()
        ]
    
    def filter_items(
        self,
        category: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Item]:
        """
        Filters items by exact category and/or status.
        
        If a parameter is omitted (None), it is not used for filtering.

        Args:
            category (Optional[str], optional): The exact category to filter by. Defaults to None.
            status (Optional[str], optional): The exact status to filter by. Defaults to None.

        Returns:
            List[Item]: Items that match the provided filters.
        """
        all_items = self.get_all_items()
        
        return [
            item for item in all_items
            if (category is None or item.category == category)
            and (status is None or item.status == status)
        ]