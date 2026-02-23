"""Core package for the Lost and Found Application.

This top-level package aggregates the primary subpackage that make up the
application backend.  It currently exposes the following components:

- :mod:`src.models` - domain entities such as :class:`~src.models.item.Item` and
  related validation logic.
- :mod:`src.controllers` - database and persistence controllers (stubbed in
documentation until implemented).
- :mod:`src.utils` - miscellaneous utility functions used across the codebase.
- :mod:`src.views` - view logic responsible for formatting or rendering data.

While most code will import directly from the appropriate submodule, a handful
of frequently used names are re-exported here for convenience.  At the moment
that includes :class:`~src.models.item.Item` and
:class:`~src.models.item.ValidationError`.

The public API provided by the package is documented below::

    .. autosummary::
       :toctree: ../api

       models
       controllers
       utils
       views

"""

from .models import Item, ValidationError  # convenience imports

__all__ = ["Item", "ValidationError"]
