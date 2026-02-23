from pathlib import Path
import sqlite3
from typing import Generator

import pytest

from src.models.database import DatabaseManager
from src.models.item import Item


@pytest.fixture(name="db")
def db_fixture(tmp_path: Path) -> Generator[DatabaseManager, None, None]:
    """
    Fixture providing a in-memory DatabaseManager fresh for each test.
    Uses Pytest's tmp_path to create an isolated, temporary database file.

    Yields:
        Iterator[DatabaseManager]: An initialized database manager hooked to ':memory:'
    """
    temp_db_path = tmp_path / 'test_lost_and_found.db'
    
    manager = DatabaseManager(db_name=str(temp_db_path))
    yield manager
    

@pytest.fixture(name="item")
def sample_item() -> Item:
    """Fixture providing a valid Item instance without an ID."""
    return Item(
        name="Yellow Beanie",
        category="Accessories",
        date="2025-11-25",
        location="Cafeteria",
        status="Lost",
        contact_info="jane.doe@university.ac.uk"
    )
    

def test_database_initialization(db: DatabaseManager) -> None:
    """Test that hte database and items table are created correctly."""
    with sqlite3.connect(db.db_name) as conn: # connect directly to schema
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table'
            AND name='items'
            """
        )
        table_exists = cursor.fetchone()
        assert table_exists is not None, "The 'items' table was not properly created."


def test_add_and_get_item(db: DatabaseManager, item: Item) -> None:
    """Test inserting an item and retrieving it."""
    # Create
    item_id = db.add_item(item)
    assert item_id > 0, "add_item should return a valid database ID greater than 0"
    
    # Read
    items = db.get_all_items()
    assert len(items) == 1
    
    fetched_item = items[0]
    assert fetched_item.id == item_id
    assert fetched_item.name == item.name
    assert fetched_item.status == item.status
    

def test_get_all_items_empty(db: DatabaseManager) -> None:
    """Test fetching items from an empty database."""
    items = db.get_all_items()
    assert isinstance(items, list)
    assert len(items) == 0
    

def test_update_item_success(db: DatabaseManager, item: Item) -> None:
    """Test updating an existing item's details."""
    item_id = db.add_item(item)

    item_to_update = db.get_all_items()[0]
    item_to_update.status = "Found"
    item_to_update.location = "Security Desk"
    
    success = db.update_item(item_to_update)
    assert success is True, "update_item should return True on successful update."
    
    updated_item = db.get_all_items()[0]
    assert updated_item.status == "Found"
    assert updated_item.location == "Security Desk"
    

def test_update_item_not_found(db: DatabaseManager, item: Item) -> None:
    """Test updating an item that odes not exist in the database."""
    item.id = 999
    success = db.update_item(item)
    assert success is False, "update_item should return False if the ID does not exist."
    

def test_delete_item_success(db: DatabaseManager, item: Item) -> None:
    """Test deleting an existing item."""
    item_id = db.add_item(item)
    
    assert len(db.get_all_items()) == 1
    
    success = db.delete_item(item_id)
    assert success is True
    
    assert len(db.get_all_items()) == 0
    
    
def test_delete_item_not_found(db: DatabaseManager) -> None:
    """Test deleting an item ID that does not exist."""
    success = db.delete_item(9999)
    assert success is False, "delete_item should return False if ID does not exist."
