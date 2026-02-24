from pathlib import Path
from typing import Generator

import pytest

from src.controllers.app_controller import AppController
from src.models.database import DatabaseManager
from src.models.item import Item


@pytest.fixture(name="controller")
def populated_controller(tmp_path: Path) -> Generator[AppController, None, None]:
    """
    Fixture providing an AppController connected to a temporary database,
    pre-populated with diverse items for testing search and filter logic.
    """
    db_path = tmp_path / "test_controller.db"
    db_manager = DatabaseManager(db_name=str(db_path))
    app_controller = AppController(db_manager)

    items_to_insert = [
        Item("Keys", "Misc", "2025-10-01", "Library", "Lost", "ann@university.ac.uk"),
        Item(
            "MacBook Pro",
            "Electronics",
            "2026-01-20",
            "Cafeteria",
            "Found",
            "barbara@university.ac.uk",
        ),
        Item(
            "Green Jacket",
            "Clothing",
            "2024-09-11",
            "Gym",
            "Lost",
            "charles@university.ac.uk",
        ),
        Item(
            "Samsung Galaxy 8",
            "Electronics",
            "2025-11-13",
            "Library",
            "Claimed",
            "devon@university.ac.uk",
        ),
    ]
    for item in items_to_insert:
        db_manager.add_item(item)

    yield app_controller


def test_search_items_by_name(controller: AppController) -> None:
    """Test searching items by a keyword present in the name (case-insensitive)."""
    results = controller.search_items("macbook")
    assert len(results) == 1
    assert results[0].name == "MacBook Pro"


def test_search_items_by_location(controller: AppController) -> None:
    """Test searching items by a keyword present in the location."""
    results = controller.search_items("library")
    assert len(results) == 2
    names = [item.name for item in results]
    assert "Keys" in names
    assert "Samsung Galaxy 8" in names


def test_search_items_no_results(controller: AppController) -> None:
    """Test searching for a keyword that does not exist."""
    results = controller.search_items("Flint")
    assert len(results) == 0


def test_search_items_empty_string(controller: AppController) -> None:
    """Test that an empty search string results all items."""
    results = controller.search_items("")
    assert len(results) == 4


def test_filter_items_by_category(controller: AppController) -> None:
    """Test filtering items strictly by category."""
    results = controller.filter_items(category="Electronics")
    assert len(results) == 2
    for item in results:
        assert item.category == "Electronics"


def test_filter_items_by_status(controller: AppController) -> None:
    """Test filtering items strictly by status."""
    results = controller.filter_items(status="Lost")
    assert len(results) == 2
    for item in results:
        assert item.status == "Lost"


def test_filter_items_combined(controller: AppController) -> None:
    """Test filtering by both category and status simultaneously."""
    results = controller.filter_items(category="Electronics", status="Found")
    assert len(results) == 1
    assert results[0].name == "MacBook Pro"


def test_filter_items_non_provided(controller: AppController) -> None:
    """Test that providing no filter arguments returns all items."""
    results = controller.filter_items()
    assert len(results) == 4
