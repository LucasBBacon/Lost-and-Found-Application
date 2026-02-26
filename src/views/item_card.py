from typing import Any, Callable, Optional

import customtkinter as ctk

from src.models.item import Item
from src.utils.theme import ThemeColors


class ItemCard(ctk.CTkFrame):

    def __init__(
        self,
        master: Any,
        item: Item,
        search_term: str,
        edit_callback: Callable,
        delete_callback: Callable,
        selection_callback: Callable,
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)
        self.item = item
        self.search_term = search_term.lower().strip()
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback
        self.selection_callback = selection_callback

        self.selected = False
        self.default_fg_color = self.cget("fg_color")

        self._build_card()
        self._bind_click_events()

    def _build_card(self) -> None:
        self.label_name = ctk.CTkLabel(
            self,
            text=self.item.name,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self._get_color(self.item.name),
        )
        self.label_name.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))

        self.label_status = ctk.CTkLabel(
            self,
            text=f"[{self.item.status}]",
            font=ctk.CTkFont(weight="bold"),
            text_color=self._get_color(self.item.status),
        )
        self.label_status.grid(row=0, column=1, sticky="e", padx=10, pady=(10, 0))

        self.label_category = ctk.CTkLabel(
            self,
            text=f"Category: {self.item.category}",
            text_color=self._get_color(self.item.category),
        )
        self.label_category.grid(row=1, column=0, sticky="w", padx=10)

        self.label_date = ctk.CTkLabel(
            self, text=f"Date: {self.item.date}", text_color=ThemeColors.TEXT_MUTED
        )
        self.label_date.grid(row=1, column=1, sticky="e", padx=10)

        self.label_location = ctk.CTkLabel(
            self,
            text=f"Location: {self.item.location}",
            text_color=self._get_color(self.item.location),
        )
        self.label_location.grid(row=2, column=0, sticky="w", padx=10, pady=(0, 10))

        self.label_contact = ctk.CTkLabel(
            self,
            text=f"Contact: {self.item.contact_info}",
            text_color=self._get_color(self.item.contact_info),
        )
        self.label_contact.grid(row=2, column=1, sticky="e", padx=10, pady=(0, 10))

        action_frame = ctk.CTkFrame(self, fg_color=ThemeColors.TRANSPARENT)
        action_frame.grid(
            row=3, column=0, columnspan=2, sticky="e", padx=10, pady=(10, 0)
        )

        button_delete = ctk.CTkButton(
            action_frame,
            text="Delete",
            width=60,
            height=24,
            fg_color=ThemeColors.BUTTON_DANGER,
            hover_color=ThemeColors.BUTTON_DANGER_HOVER,
            command=lambda: self.delete_callback(self.item),
        )
        button_delete.pack(side="right", padx=(5, 0))

        button_delete = ctk.CTkButton(
            action_frame,
            text="Edit",
            width=60,
            height=24,
            command=lambda: self.edit_callback(self.item),
        )
        button_delete.pack(side="right")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def _get_color(self, field_value: str) -> Optional[str]:
        if self.search_term and self.search_term in field_value.lower():
            return ThemeColors.HIGHLIGHT
        return None

    def _bind_click_events(self) -> None:
        clickable_widgets = [
            self,
            self.label_name,
            self.label_status,
            self.label_category,
            self.label_date,
            self.label_location,
            self.label_contact,
        ]
        for widget in clickable_widgets:
            widget.bind("<Button-1>", self._toggle_selection)

    def _toggle_selection(self, event) -> None:
        self.selected = not self.selected
        new_color = ThemeColors.CARD_SELECTED if self.selected else self.default_fg_color
        self.configure(fg_color=new_color)

        self.selection_callback()
