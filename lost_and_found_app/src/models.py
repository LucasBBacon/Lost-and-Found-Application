from datetime import datetime
from enum import Enum
from typing import Optional


class ItemStatus(str, Enum):
    """
    Represents the possible states of an item using enumeration.
    Inherting from the string primitive to allow for easier storage in SQLite.
    """
    LOST = "Lost"
    FOUND = "Found"
    CLAIMED = "Claimed"

class Item:
    """
    Represents a lost or found item within the system.
    
    Attributes:
        id (Optional[int]): Unique Identifier for the current item.
        name (str): The name or short description for the current item.
        category (str): The category the current item belongs to.
        date_lost (str): The date the item was lost or found (Format: YYYY-MM-DD).
        location (str): Where the item was lost or found.
        status (ItemStatus): The status of the current item.
        contact_info (str): Contact details for the finder or owner.
    """
    def __init__(self, 
                 name: str, 
                 category: str, 
                 date_lost: str, 
                 location: str, 
                 status: ItemStatus, 
                 contact_info: str, 
                 item_id: Optional[int] = None) -> None:
        """
        Initializes a new Item with validation.

        Args:
            name (str): Name of the current item.
            category (str): Category of the current item.
            date_lost (str): Date string in YYYY-MM-DD format.
            location (str): Location where item was lost or found.
            status (ItemStatus): Current status of item (Lost, Found, Claimed).
            contact_info (str): Email or phone number of contact for item.
            item_id (Optional[int], optional): Database ID for item. Defaults to None.
        """
        self.id: Optional[int] = item_id
        self.name: str = name
        self.category: str = category
        self.date_lost = date_lost
        self.location = location
        self.status = status
        self.contact_info = contact_info
        
        self._validate()
       
    def _validate(self) -> None:
        """
        Validates any fields in the Item.

        Checks:
         - Required fields are not empty.
         - Date string matches the required YYYY-MM-DD format.

        Raises:
            ValueError: If any validation check fails.
        """
        if not self.name or not self.name.strip():
            raise ValueError("Item name field is required.")
        if not self.location or not self.location.strip():
            raise ValueError("Item location field is required.")
        if not self.contact_info or not self.contact_info.strip():
            raise ValueError("Contact info field is required.")
        
        try:
            datetime.strptime(self.date_lost, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {self.date_lost}. Expected format: YYYY-MM-DD.")
        
    def update_status(self, new_status: ItemStatus) -> None:
        """
        Update the status of the current item.

        Args:
            new_status (ItemStatus): The new status to set.
        """
        self.status = new_status