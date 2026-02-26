from typing import Callable, Optional

import customtkinter as ctk

from src.controllers.app_controller import AppController
from src.models.item import Item, ValidationError
from src.utils.theme import ThemeColors


class ItemFormWindow(ctk.CTkToplevel):
    def __init__(
        self,
        master,
        controller: AppController,
        on_success: Callable,
        item: Optional[Item] = None,
    ) -> None:
        super().__init__(master)
        self.controller = controller
        self.on_success = on_success
        self.item = item

        title_text = "Edit Item" if self.item else "Add New Item"
        self.title(title_text)
        self.geometry("400x550")

        self.transient(master)
        self.grab_set()

        self._setup_form()
        if self.item:
            self._prefill_data()

    def _setup_form(self) -> None:
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Item Name *").pack(anchor="w", pady=(10, 0))
        self.entry_name = ctk.CTkEntry(frame, width=350)
        self.entry_name.pack(fill="x")

        ctk.CTkLabel(frame, text="Category *").pack(anchor="w", pady=(10, 0))
        self.opt_category = ctk.CTkOptionMenu(
            frame, values=["Electronics", "Clothing", "Books", "Misc"]
        )
        self.opt_category.pack(fill="x")

        ctk.CTkLabel(frame, text="Date (YYYY-MM-DD) *").pack(anchor="w", pady=(10, 0))
        self.entry_date = ctk.CTkEntry(frame, width=350)
        self.entry_date.pack(fill="x")

        ctk.CTkLabel(frame, text="Location *").pack(anchor="w", pady=(10, 0))
        self.entry_location = ctk.CTkEntry(frame, width=350)
        self.entry_location.pack(fill="x")

        ctk.CTkLabel(frame, text="Status *").pack(anchor="w", pady=(10, 0))
        self.opt_status = ctk.CTkOptionMenu(frame, values=["Lost", "Found", "Claimed"])
        self.opt_status.pack(fill="x")

        ctk.CTkLabel(frame, text="Contact Info *").pack(anchor="w", pady=(10, 0))
        self.entry_contact = ctk.CTkEntry(frame, width=350)
        self.entry_contact.pack(fill="x")

        self.label_error = ctk.CTkLabel(
            frame, text="", text_color=ThemeColors.TEXT_ERROR
        )
        self.label_error.pack(pady=(10, 0))

        button_frame = ctk.CTkFrame(frame, fg_color=ThemeColors.TRANSPARENT)
        button_frame.pack(fill="x", pady=(20, 0))

        ctk.CTkButton(
            button_frame, text="Cancel", command=self.destroy, fg_color="gray"
        ).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(button_frame, text="Save", command=self._save_item).pack(
            side="right", expand=True, padx=5
        )

    def _prefill_data(self) -> None:
        if self.item is None:
            return
        self.entry_name.insert(0, self.item.name)
        self.opt_category.set(self.item.category)
        self.entry_date.insert(0, self.item.date)
        self.entry_location.insert(0, self.item.location)
        self.opt_status.set(self.item.status)
        self.entry_contact.insert(0, self.item.contact_info)

    def _save_item(self) -> None:
        try:
            new_item_data = Item(
                name=self.entry_name.get(),
                category=self.opt_category.get(),
                date=self.entry_date.get(),
                location=self.entry_location.get(),
                status=self.opt_status.get(),
                contact_info=self.entry_contact.get(),
            )

            if self.item:
                new_item_data.id = self.item.id
                self.controller.update_item(new_item_data)
            else:
                self.controller.add_item(new_item_data)

            self.on_success()
            self.destroy()

        except ValidationError as e:
            self.label_error.configure(text=str(e))
