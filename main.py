"""
Lost and Found Application Entry Point

This module serves as the main entry point for the Lost and Found Application.
It initializes the database, controller, and GUI components, then starts the
application event loop.
"""

import sys
from pathlib import Path

# Add src directory to Python path for proper imports
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path.parent))

from src.models.database import DatabaseManager
from src.controllers.app_controller import AppController
from src.views.view import AppView


def main() -> None:
    """
    Initialize and run the Lost and Found Application.

    This function:
    1. Creates a DatabaseManager instance with the default database
    2. Initializes the AppController with the database manager
    3. Creates the main application window (AppView)
    4. Starts the GUI event loop
    """
    # Initialize the database manager
    db_manager = DatabaseManager("lost_and_found.db")

    # Initialize the application controller
    controller = AppController(db_manager)

    # Create and run the main application window
    app = AppView(controller)
    app.mainloop()


if __name__ == "__main__":
    main()
