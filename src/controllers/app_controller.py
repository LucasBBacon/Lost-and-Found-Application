from typing import List, Optional

from src.models.database import DatabaseManager
from src.models.item import Item


class AppController:
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db = db_manager
    
    def add_item(self, item: Item) -> int:
        return 0
    
    def get_all_items(self) -> List[Item]:
        return []
    
    def update_item(self, item: Item) -> bool:
        return False
    
    def delete_item(self, item_id: int) -> bool:
        return False
    
    def search_items(self, keyword: str) -> List[Item]:
        return []
    
    def filter_items(
        self,
        category: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Item]:
        return []