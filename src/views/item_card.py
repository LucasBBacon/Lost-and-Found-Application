from typing import Any, Callable, Optional

import customtkinter as ctk

from src.models.item import Item


class ItemCard(ctk.CTkFrame):

    HIGHLIGHT_COLOR = "#2FA672"

    def __init__(
        self,
        master: Any,
        item: Item,
        search_term: str,
        edit_callback: Callable,
        delete_callback: Callable,
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)
        self.item = item
        self.search_term = search_term.lower().strip()
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback

        self._build_card()

    def _build_card(self) -> None:
        self.lbl_name = ctk.CTkLabel(
            self,
            text=self.item.name,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self._get_color(self.item.name),
        )
        self.lbl_name.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))

        self.lbl_status = ctk.CTkLabel(
            self,
            text=f"[{self.item.status}]",
            font=ctk.CTkFont(weight="bold"),
            text_color=self._get_color(self.item.status),
        )
        self.lbl_status.grid(row=0, column=1, sticky="e", padx=10, pady=(10, 0))

        self.lbl_category = ctk.CTkLabel(
            self,
            text=f"Category: {self.item.category}",
            text_color=self._get_color(self.item.category),
        )
        self.lbl_category.grid(row=1, column=0, sticky="w", padx=10)

        self.lbl_date = ctk.CTkLabel(
            self, text=f"Date: {self.item.date}", text_color="gray"
        )
        self.lbl_date.grid(row=1, column=1, sticky="e", padx=10)

        self.lbl_location = ctk.CTkLabel(
            self,
            text=f"Location: {self.item.location}",
            text_color=self._get_color(self.item.location),
        )
        self.lbl_location.grid(row=2, column=0, sticky="w", padx=10, pady=(0, 10))

        self.lbl_contact = ctk.CTkLabel(
            self,
            text=f"Contact: {self.item.contact_info}",
            text_color=self._get_color(self.item.contact_info),
        )
        self.lbl_contact.grid(row=2, column=1, sticky="e", padx=10, pady=(0, 10))

        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(
            row=3, column=0, columnspan=2, sticky="e", padx=10, pady=(10, 0)
        )

        btn_delete = ctk.CTkButton(
            action_frame,
            text="Delete",
            width=60,
            height=24,
            fg_color="#D9534F",
            command=lambda: self.delete_callback(self.item),
        )
        btn_delete.pack(side="right", padx=(5, 0))

        btn_delete = ctk.CTkButton(
            action_frame,
            text="Edit",
            width=60,
            height=24,
            command=lambda: self.edit_callback(self.item),
        )
        btn_delete.pack(side="right")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
    def _get_color(self, field_value: str) -> Optional[str]:
        if self.search_term and self.search_term in field_value.lower():
            return self.HIGHLIGHT_COLOR
        return None
