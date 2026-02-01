import pytest

from lost_and_found_app.src import *


def test_create_valid_item():
    """
    Test that an item can be created with all valid fields.
    """
    item = Item(name="Pink Umbrella",
                category="Personal Accessories",
                date_lost="2025-03-20",
                location="Library",
                status=ItemStatus.LOST,
                contact_info="student@thisuni.ac.uk")
    
    assert item.name == "Pink Umbrella"
    assert item.category == "Personal Accessories"
    assert item.date_lost == "2025-03-20"
    assert item.location == "Library"
    assert item.status == ItemStatus.LOST
    assert item.contact_info == "student@thisuni.ac.uk"
    

def test_date_validation_format():
    """
    Test that entering an invalid date format for item raises an error.
    """
    with pytest.raises(ValueError):
        Item(name="Phone",
             category="Electronics",
             date_lost="25-10-2025",
             location="Lecture Hall",
             status=ItemStatus.LOST,
             contact_info="12345")


def test_missing_required_field():
    """
    Test that missing a required field when creating item raises an error.
    """
    with pytest.raises(ValueError):
        Item(name="",
             category="Electronics",
             date_lost="2025-11-05",
             location="Gym",
             status=ItemStatus.LOST,
             contact_info="12345")


def test_update_status():
    """
    Test that the status of an item can be updated.
    """
    item = Item(name="Keys",
                category="Misc",
                date_lost="2025-01-23",
                location="Reception",
                status=ItemStatus.FOUND,
                contact_info="admin@uni.edu")
    
    item.update_status(ItemStatus.CLAIMED)
    assert item.status == ItemStatus.CLAIMED