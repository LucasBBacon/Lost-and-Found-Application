from typing import Callable, List

import customtkinter as ctk

from src.models.item import Item
from src.utils.theme import ThemeColors


class ConfirmDeleteWindow(ctk.CTkToplevel):

    def __init__(self, master, items: List[Item], on_confirm: Callable) -> None:
        super().__init__(master)
        self.items = items
        self.on_confirm = on_confirm

        self.title("Confirm Deletion")
        self.geometry("350x250")
        self.transient(master)
        self.grab_set()

        self._setup_ui()

    def _setup_ui(self) -> None:
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        count = len(self.items)
        msg = f"Are you sure you want to delete {count} item{'s' if count > 1 else ''}?\n\n"

        for item in self.items[:3]:
            msg += f"- {item.name}\n"
        if count > 3:
            msg += f"... and {count - 3} more."

        label_message = ctk.CTkLabel(frame, text=msg, justify="left", wraplength=300)
        label_message.pack(pady=(10, 20))

        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(fill="x", side="bottom", pady=10)

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            fg_color=ThemeColors.BUTTON_CANCEL,
        ).pack(side="left", expand=True, padx=5)

        ctk.CTkButton(
            button_frame,
            text="Delete",
            command=self._execute_delete,
            fg_color=ThemeColors.BUTTON_DANGER,
            hover_color=ThemeColors.BUTTON_DANGER_HOVER,
        ).pack(side="right", expand=True, padx=5)

    def _execute_delete(self) -> None:
        self.on_confirm(self.items)
        self.destroy()
