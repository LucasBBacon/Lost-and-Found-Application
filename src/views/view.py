import tkinter as tk
import customtkinter as ctk

from src.controllers.app_controller import AppController
from src.models.database import DatabaseManager
from src.models.item import Item
from src.views.item_card import ItemCard
from src.views.item_form import ItemFormWindow


class AppView(ctk.CTk):
    def __init__(self, controller: AppController):
        super().__init__()
        self.controller = controller

        self.title("Lost and Found Application")
        self.geometry("800x600")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_filter_change)

        self.category_var = ctk.StringVar(value="All")
        self.status_var = ctk.StringVar(value="All")

        self._setup_menu()
        self._setup_control_panel()
        self._setup_main_display()
        self._setup_action_panel()

        self._refresh_display()

    def _setup_menu(self) -> None:
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Add New Item", command=self._mock_add_item)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Clear Filters", command=self._clear_filters)
        menubar.add_cascade(label="View", menu=view_menu)

        self.config(menu=menubar)

    def _setup_control_panel(self) -> None:
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(side="top", fill="x", padx=10, pady=10)

        search_entry = ctk.CTkEntry(
            control_frame,
            textvariable=self.search_var,
            placeholder_text="Search name, location, contact...",
            width=300,
        )
        search_entry.pack(side="left", padx=10, pady=10)

        status_menu = ctk.CTkOptionMenu(
            control_frame,
            variable=self.status_var,
            values=["All", "Lost", "Found", "Claimed"],
            command=self._on_filter_change,
        )
        status_menu.pack(side="right", padx=10, pady=10)

        category_menu = ctk.CTkOptionMenu(
            control_frame,
            variable=self.category_var,
            values=["All", "Electronics", "Clothing", "Books", "Misc"],
            command=self._on_filter_change,
        )
        category_menu.pack(side="right", padx=10, pady=10)

    def _setup_main_display(self) -> None:
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(
            side="top", fill="both", expand=True, padx=10, pady=(0, 10)
        )

    def _setup_action_panel(self) -> None:
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
        
        btn_add = ctk.CTkButton(action_frame, text="[+] Add Item", command=self._open_add_form)
        btn_add.pack(side="left", padx=10)
        
        btn_edit = ctk.CTkButton(action_frame, text="[/] Edit Selected", state="disabled")
        btn_edit.pack(side="left", padx=10)

    def _on_filter_change(self, *args) -> None:
        self._refresh_display()

    def _clear_filters(self) -> None:
        self.search_var.set("")
        self.category_var.set("All")
        self.status_var.set("All")

    def _refresh_display(self) -> None:
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        search_term = self.search_var.get()
        category = self.category_var.get() if self.category_var.get() != "All" else None
        status = self.status_var.get() if self.status_var.get() != "All" else None

        items = self.controller.search_items(search_term)

        filtered_items = [
            item
            for item in items
            if (category is None or item.category == category)
            and (status is None or item.status == status)
        ]

        for item in filtered_items:
            card = ItemCard(
                self.scroll_frame,
                item,
                search_term,
                edit_callback=self._open_edit_form,
                delete_callback=self._delete_item
            )
            card.pack(fill="x", padx=5, pady=5)

    def _mock_add_item(self) -> None:
        from datetime import datetime

        dummy = Item(
            name=f"New Item {datetime.now().second}",
            category="Misc",
            date="2025-10-30",
            location="Campus",
            status="Lost",
            contact_info="test@university.ac.uk",
        )
        self.controller.add_item(dummy)
        self._refresh_display()
        
    def _open_add_form(self) -> None:
        ItemFormWindow(self, self.controller, on_success=self._refresh_display)
        
    def _open_edit_form(self, item: Item) -> None:
        ItemFormWindow(self, self.controller, on_success=self._refresh_display, item=item)
        
    def _delete_item(self, item: Item) -> None:
        if item.id is not None:
            self.controller.delete_item(item.id)
            self._refresh_display()


if __name__ == "__main__":
    db_manager = DatabaseManager("lost_and_found.db")
    controller = AppController(db_manager)

    app = AppView(controller)
    app.mainloop()
