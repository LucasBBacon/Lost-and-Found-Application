from typing import List

from src.models.item import Item


class DatabaseManager:
    def __init__(self, db_name: str = "lost_and_found.db") -> None:
        self.db_name = db_name
        
    def _initialize_db(self) -> None:
        pass
    
    def add_item(self, item: Item) -> int:
        return 0
    
    def get_all_items(self) -> List[Item]:
        return []
    
    def update_item(self, item: Item) -> bool:
        return False
    
    def delete_item(self, item_id: int) -> bool:
        return False