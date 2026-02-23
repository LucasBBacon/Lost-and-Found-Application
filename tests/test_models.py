"""Unit tests for the domain models."""

from datetime import date, timedelta

import pytest

from src.models.item import Item, ValidationError


@pytest.fixture(name="valid_item")
def valid_item_data() -> dict:
    """
    Fixture providing a dictionary of valid item data.

    Returns:
        dict: A dictionary containing valid kwargs for an Item.
    """
    return {
        "name": "Black iPhone 13",
        "category": "Electronics",
        "date": "2023-10-25",
        "location": "Library",
        "status": "Found",
        "contact_info": "john.doe@university.ac.uk"
    }
    

def test_create_valid_item(valid_item: dict) -> None:
    """Test that an Item can be created with valid data."""
    item = Item(**valid_item)
    
    assert item.name == "Black iPhone 13"
    assert item.category == "Electronics"
    assert item.date == "2023-10-25"
    assert item.location == "Library"
    assert item.status == "Found"
    assert item.contact_info == "john.doe@university.ac.uk"


@pytest.mark.parametrize("missing_field", [
    "name", "category", "date", "location", "status", "contact_info"
])
def test_item_missing_required_fields(valid_item: dict, missing_field: str) -> None:
    """
    Test that missing or empty required fields raise a ValidationError

    Args:
        valid_item (dict): The valid item data fixture.
        missing_field (str): The field to empty out for the test.
    """
    valid_item[missing_field] = "   " # Test with empty string
    with pytest.raises(ValidationError, match=f"Field '{missing_field}' cannot be empty"):
        Item(**valid_item)
        
    valid_item[missing_field] = None # Test with None
    with pytest.raises(ValidationError, match=f"Field '{missing_field}' cannot be empty"):
        Item(**valid_item)
    

@pytest.mark.parametrize("invalid_date", [
    "25-10-2023", # Wrong format (DD-MM-YYYY)
    "2023/10/25", # Wrong separator
    "Not a date", # Arbitrary string
    "2023-13-10", # Invalid month
    "2023-12-45", # Invalid day
    "2023-43-41", # Invalid month and day
])    
def test_item_invalid_date_format(valid_item: dict, invalid_date: str) -> None:
    """
    Test that invalid date formats raise a ValidationError.

    Args:
        valid_item (dict): The valid item data fixture.
        invalid_date (str): An invalid date string.
    """
    valid_item["date"] = invalid_date
    with pytest.raises(ValidationError, match="Date must be in YYYY-MM-DD format"):
        Item(**valid_item)


def test_item_future_date_invalid(valid_item: dict) -> None:
    """Tes that providing a date in the future raises a ValidationError."""
    future_date = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    valid_item["date"] = future_date
    
    with pytest.raises(ValidationError, match=f"Date cannot be in the future"):
        Item(**valid_item)
        

@pytest.mark.parametrize("invalid_status", [
    "Stolen",
    "Pending",
    "RandomStatus",
])
def test_item_invalid_status(valid_item: dict, invalid_status: str) -> None:
    """
    Test that invalid statuses raises a ValidationError.
    Allowed statuses should be 'Lost', 'Found', or 'Claimed'.

    Args:
        valid_item (dict): The valid item data fixture.
        invalid_status (str): An unrecognised status.
    """
    valid_item["status"] = invalid_status
    with pytest.raises(ValidationError, match="Status must be 'Lost', 'Found', or 'Claimed'"):
        Item(**valid_item)
