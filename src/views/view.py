import tkinter as tk
from typing import List
import customtkinter as ctk

from src.controllers.app_controller import AppController
from src.models.database import DatabaseManager
from src.models.item import Item
from src.utils.theme import ThemeColors
from src.views.confirm_delete import ConfirmDeleteWindow
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

        btn_add = ctk.CTkButton(
            action_frame, text="[+] Add Item", command=self._open_add_form
        )
        btn_add.pack(side="left", padx=10)

        self.btn_edit_selected = ctk.CTkButton(
            action_frame,
            text="[/] Edit Selected",
            state="disabled",
            command=self._prompt_edit_selected,
        )
        self.btn_edit_selected.pack(side="left", padx=10)

        self.btn_delete_selected = ctk.CTkButton(
            action_frame,
            text="[X] Delete Selected",
            fg_color=ThemeColors.BUTTON_DANGER,
            hover_color=ThemeColors.BUTTON_DANGER_HOVER,
            state="disabled",
            command=self._prompt_batch_delete,
        )
        self.btn_delete_selected.pack(side="left", padx=10)

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
                delete_callback=self._delete_item,
                selection_callback=self._on_card_selection_change,
            )
            card.pack(fill="x", padx=5, pady=5)

        self._on_card_selection_change()

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
        ItemFormWindow(
            self, self.controller, on_success=self._refresh_display, item=item
        )

    def _prompt_edit_selected(self) -> None:
        selected_items = [
            card.item
            for card in self.scroll_frame.winfo_children()
            if isinstance(card, ItemCard) and card.selected
        ]

        if len(selected_items) == 1:
            self._open_edit_form(selected_items[0])

    def _delete_item(self, item: Item) -> None:
        if item.id is not None:
            self.controller.delete_item(item.id)
            self._refresh_display()

    def _on_card_selection_change(self) -> None:
        selected_items = [
            card.item
            for card in self.scroll_frame.winfo_children()
            if isinstance(card, ItemCard) and card.selected
        ]
        count = len(selected_items)

        self.btn_edit_selected.configure(state="normal" if count == 1 else "disabled")
        self.btn_delete_selected.configure(state="normal" if count > 0 else "disabled")

    def _prompt_single_delete(self, item: Item) -> None:
        ConfirmDeleteWindow(self, [item], on_confirm=self._execute_deletions)

    def _prompt_batch_delete(self) -> None:
        selected_items = [
            card.item
            for card in self.scroll_frame.winfo_children()
            if isinstance(card, ItemCard) and card.selected
        ]
        if selected_items:
            ConfirmDeleteWindow(
                self, selected_items, on_confirm=self._execute_deletions
            )

    def _execute_deletions(self, item_to_delete: List[Item]) -> None:
        for item in item_to_delete:
            if item.id is not None:
                self.controller.delete_item(item.id)
        self._refresh_display()


if __name__ == "__main__":
    db_manager = DatabaseManager("lost_and_found.db")
    controller = AppController(db_manager)

    app = AppView(controller)
    app.mainloop()
