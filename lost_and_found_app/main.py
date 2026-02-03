import tkinter as tk

from src import InventoryManager
from src import LostFoundApp


def main():
    db_manager = InventoryManager("lost_and_found.db")
    db_manager.initialize_db()
    
    app = LostFoundApp(None, db_manager)
    
    try:
        app.mainloop()
    finally:
        db_manager.close()
        
if __name__ == "__main__":
    main()
    