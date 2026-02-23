"""Domain model Item for the Lost and Found Application."""

from dataclasses import dataclass
from datetime import datetime


class ValidationError(Exception):
    """Custom exception raised for invalid item data."""

    pass


@dataclass
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

    name: str
    category: str
    date: str
    location: str
    status: str
    contact_info: str

    def __post_init__(self) -> None:
        """Automatically called after initialization to validate attributes."""
        self._validate()

    def _validate(self) -> None:
        """
        Runs all validation rules against the item's properties.

        Raises:
            ValidationError: If any property is invalid, missing, or improperly formatted.
        """
        self._validate_required_fields()
        self._validate_date()
        self._validate_status()

    def _validate_required_fields(self):
        """Checks that no fields are None or empty strings."""
        fields_to_check = {
            "name": self.name,
            "category": self.category,
            "date": self.date,
            "location": self.location,
            "status": self.status,
            "contact_info": self.contact_info,
        }

        for field_name, value in fields_to_check.items():
            if value is None or (isinstance(value, str) and not value.strip()):
                raise ValidationError(f"Field '{field_name}' cannot be empty")

    def _validate_date(self) -> None:
        """Checks that the date is in the correct format and not in the future."""
        try:
            parsed_date = datetime.strptime(self.date, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError("Date must be in YYYY-MM-DD format")
        
        if parsed_date > datetime.now().date():
            raise ValidationError("Date cannot be in the future")

    def _validate_status(self) -> None:
        """Checks that the status is one of the allowed values."""
        allowed_statuses = {"Lost", "Found", "Claimed"}
        if self.status not in allowed_statuses:
            raise ValidationError("Status must be 'Lost', 'Found', or 'Claimed'")
