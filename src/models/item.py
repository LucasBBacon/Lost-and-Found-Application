"""Domain model Item for the Lost and Found Applicaiton."""

class ValidationError(Exception):
    """Custom exception raised for invalid item data."""
    pass


class Item:
    """
    Represents a lost or found item.
    
    Attributes:
        name (str): The name of the item.
        category (str): The category of the item (e.g., electronics, clothing).
        date (str): The date the item was lost or found (YYYY-MM-DD).
        location (str): Where the item was lost or found.
        status (str): The current status of the item.
        contact_info (str): Contact information of the person reporting.
    """
    
    def __init__(
        self,
        name: str,
        category: str,
        date: str,
        location: str,
        status: str,
        contact_info: str
    ) -> None:
        self.name = name
        self.category = category 
        self.date = date 
        self.location = location 
        self.status = status 
        self.contact_info = contact_info
