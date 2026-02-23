"""Models package for the Lost and Found Application.

This package defines the domain objects used throughout the
application backend.  At present it includes the :class:`Item`
model and the associated :class:`ValidationError` exception used
when invalid data is supplied.  The package is designed to be
lightweight and decoupled from any particular persistence layer
or web framework, making it easy to import wherever the core
business logic needs access to the item representation.

The public API exposed by this package is:

.. autosummary::
   :toctree: ../api

   Item
   ValidationError
   DatabaseManager
"""

from .item import Item, ValidationError
from .database import DatabaseManager

__all__ = [
    "Item", "ValidationError",
    "DatabaseManager"
]
