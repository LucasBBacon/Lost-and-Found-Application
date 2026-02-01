import pytest

from src import *


@pytest.fixture
def manager():
    mgr = InventoryManager(db_name=":memory:")
    mgr.initialize_db()
    return mgr


def test_add_and_retrieve_item(manager):
    """
    Test adding an item and retrieve it from the database.
    """
    item = Item("Laptop",
                "Electronics",
                "2025-10-20",
                "Lab",
                ItemStatus.LOST,
                "john@email.com")
    manager.add_item(item)
    
    all_items = manager.get_all_items()
    assert len(all_items) == 1
    assert all_items[0].name == "Laptop"
    
def test_search_by_keyword(manager):
    """
    Test searching for an item by keyword.
    """
    item_a = Item("Checkered Scarf", 
                  "Clothing", 
                  "2025-09-20", "Hall A", 
                  ItemStatus.LOST, 
                  "A")
    item_b = Item("Blue Bottle", 
                  "Misc", 
                  "2023-03-10", 
                  "Hall B", 
                  ItemStatus.LOST, 
                  "B")
    
    manager.add_item(item_a)
    manager.add_item(item_b)
    
    results = manager.search_items("Scarf")
    assert len(results) == 1
    assert results[0].name == "Red Scarf"

def test_filter_by_status(manager):
    """
    Test filtering items by their status.
    """
    item_a = Item("Wallet", 
                  "Personal", 
                  "2025-05-05", 
                  "Hall A", 
                  ItemStatus.LOST, 
                  "A")
    item_b = Item("Keys", 
                  "Personal", 
                  "2025-01-02", 
                  "Hall B", 
                  ItemStatus.CLAIMED, 
                  "B")
    
    manager.add_item(item_a)
    manager.add_item(item_b)
    
    lost_items = manager.filter_by_status(ItemStatus.LOST)
    assert len(lost_items) == 1
    assert lost_items[0].name == "Wallet"

def test_delete_item(manager):
    """
    Test deleting an item.
    """
    item = Item("Old Hat", 
                "Clothing", 
                "2023-10-20", 
                "Hall A", 
                ItemStatus.LOST, 
                "A")
    manager.add_item(item)
    
    items_before = manager.get_all_items()
    item_id = items_before[0].id
    
    manager.delete_item(item_id)
    
    items_after = manager.get_all_items()
    assert len(items_after) == 0