from dataclasses import dataclass
from pathlib import Path
from typing import Any, Tuple, Union

import customtkinter as ctk


Color = Union[str, Tuple[str, str]]


@dataclass
class TestThemeColors:
    surface: Color = ("#ffffff", "#1f1f1f")
    border_subtle: Color = ("#cccccc", "#3A3A3A")
    text_primary: Color = ("#000000", "#f2f2f2")
    text_muted: Color = ("#666666", "#a0a0a0")
    danger: Color = "#d9534f"
    danger_hover: Color = "#c9302c"
    transparent: Color = "transparent"


@dataclass
class TestThemeSizes:
    item_card_width: int = 400
    item_card_height: int = 370
    item_card_padding: int = 20
    font_size_large: int = 24
    font_size_medium: int = 16
    item_card_element_padding_x: int = 20
    item_card_element_padding_y: int = 20
    text_padding_y: int = 0
    text_icon_width: int = 3


class ItemCardWireframe(ctk.CTkFrame):
    def __init__(self, master: Any, **kwargs) -> None:
        super().__init__(
            master,
            width=TestThemeSizes.item_card_width,
            height=TestThemeSizes.item_card_height,
            border_color=TestThemeColors.border_subtle,
            border_width=1,
            corner_radius=10,
            fg_color=TestThemeColors.surface,
            **kwargs
        )
        self._build_wireframe()
        self.grid_propagate(False)

    def _build_wireframe(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # region Item Name
        self.label_name = ctk.CTkLabel(
            self,
            text="Item Name",
            font=ctk.CTkFont(size=TestThemeSizes.font_size_large, weight="bold"),
        )
        self.label_name.grid(
            row=0,
            column=0,
            sticky="w",
            padx=TestThemeSizes.item_card_element_padding_x,
            pady=(TestThemeSizes.item_card_element_padding_y, 0),
        )
        # endregion

        # region Status
        self.test_frame = ctk.CTkFrame(
            self,
            width=150,
            height=30,
            corner_radius=0,
            fg_color=TestThemeColors.text_primary,
        )
        self.test_frame.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(0, TestThemeSizes.item_card_element_padding_x),
        )

        self.label_status = ctk.CTkLabel(
            self.test_frame,
            text="[Status]",
            font=ctk.CTkFont(weight="bold"),
            anchor="e",
            text_color=TestThemeColors.surface,
        )
        self.label_status.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(0, TestThemeSizes.item_card_element_padding_x),
            pady=(TestThemeSizes.item_card_element_padding_y, 0),
        )
        # endregion

        # region Category
        self.tag_label = ctk.CTkLabel(
            self,
            text="\U0001f3f7",
            font=ctk.CTkFont(size=16),
            text_color=TestThemeColors.text_muted,
        )
        self.tag_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=(TestThemeSizes.item_card_element_padding_x, 0),
            pady=TestThemeSizes.text_padding_y,
        )

        self.label_category = ctk.CTkLabel(
            self,
            text="[Category]",
            text_color=TestThemeColors.text_muted,
            font=ctk.CTkFont(size=12),
        )
        self.label_category.grid(
            row=1,
            column=0,
            sticky="w",
            padx=(TestThemeSizes.item_card_element_padding_x + 20, 0),
            pady=TestThemeSizes.text_padding_y,
        )
        # endregion

        # region Description
        self.label_description = ctk.CTkLabel(
            self,
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            text_color=TestThemeColors.text_muted,
            wraplength=360,
            justify="left",
        )
        self.label_description.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="w",
            padx=TestThemeSizes.item_card_element_padding_x,
            pady=(30, TestThemeSizes.text_padding_y),
        )
        # endregion

        # region Date And Location
        self.frame_date_location = ctk.CTkFrame(
            self, fg_color="#ee0000", corner_radius=0
        )
        self.frame_date_location.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=TestThemeSizes.item_card_element_padding_x,
            pady=(30, TestThemeSizes.text_padding_y),
        )

        self.label_date_icon = ctk.CTkLabel(
            self.frame_date_location,
            text="\U0001f4c5",
            font=ctk.CTkFont(size=18),
            text_color=TestThemeColors.text_primary,
        )
        self.label_date_icon.grid(
            row=0,
            column=0,
            sticky="w",
            pady=TestThemeSizes.text_padding_y,
        )

        self.label_date = ctk.CTkLabel(
            self.frame_date_location,
            text="[YYYY-MM-DD]",
            text_color=TestThemeColors.text_primary,
            font=ctk.CTkFont(size=14),
        )
        self.label_date.grid(
            row=0,
            column=1,
            sticky="w",
            padx=(TestThemeSizes.text_icon_width, 0),
            pady=TestThemeSizes.text_padding_y,
        )

        self.label_location_icon = ctk.CTkLabel(
            self.frame_date_location,
            text="\U0001f4cd",
            font=ctk.CTkFont(size=18),
            text_color=TestThemeColors.text_primary,
        )
        self.label_location_icon.grid(
            row=1,
            column=0,
            sticky="w",
            pady=TestThemeSizes.text_padding_y,
        )

        self.label_location = ctk.CTkLabel(
            self.frame_date_location,
            text="[Location]",
            text_color=TestThemeColors.text_primary,
            font=ctk.CTkFont(size=14),
        )
        self.label_location.grid(
            row=1,
            column=1,
            sticky="w",
            padx=(TestThemeSizes.text_icon_width, 0),
            pady=TestThemeSizes.text_padding_y,
        )
        # endregion

        # region Separator
        self.separator = ctk.CTkFrame(
            self, height=2, fg_color=TestThemeColors.border_subtle, corner_radius=0
        )
        self.separator.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=TestThemeSizes.item_card_element_padding_x,
            pady=TestThemeSizes.text_padding_y,
        )
        # endregion

        # region Contact Name
        self.label_contact_name = ctk.CTkLabel(
            self,
            text="[Contact Name]",
            text_color=TestThemeColors.text_primary,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.label_contact_name.grid(
            row=6,
            column=0,
            sticky="w",
            padx=(TestThemeSizes.item_card_element_padding_x, 0),
            pady=TestThemeSizes.text_padding_y,
        )
        # endregion

        # region Contact Info
        self.label_contact_phone_icon = ctk.CTkLabel(
            self,
            text="\U0001f4de",
            font=ctk.CTkFont(size=18),
            text_color=TestThemeColors.text_primary,
        )
        self.label_contact_phone_icon.grid(
            row=7,
            column=0,
            sticky="w",
            padx=(TestThemeSizes.item_card_element_padding_x, 0),
            pady=TestThemeSizes.text_padding_y,
        )

        self.label_contact_phone = ctk.CTkLabel(
            self,
            text="[Phone Number]",
            text_color=TestThemeColors.text_primary,
            font=ctk.CTkFont(size=14),
        )
        self.label_contact_phone.grid(
            row=7,
            column=0,
            sticky="w",
            padx=(TestThemeSizes.item_card_element_padding_x + 20, 0),
            pady=TestThemeSizes.text_padding_y,
        )

        self.label_contact_email_icon = ctk.CTkLabel(
            self,
            text="\U0001f4e7",
            font=ctk.CTkFont(size=18),
            text_color=TestThemeColors.text_primary,
        )
        self.label_contact_email_icon.grid(
            row=8,
            column=0,
            sticky="w",
            padx=(TestThemeSizes.item_card_element_padding_x, 0),
            pady=TestThemeSizes.text_padding_y,
        )

        self.label_contact_email = ctk.CTkLabel(
            self,
            text="[Email Address]",
            text_color=TestThemeColors.text_primary,
            font=ctk.CTkFont(size=14),
        )
        self.label_contact_email.grid(
            row=8,
            column=0,
            sticky="w",
            padx=(TestThemeSizes.item_card_element_padding_x + 20, 0),
            pady=TestThemeSizes.text_padding_y,
        )
        # endregion

        self.rowconfigure(9, weight=1)  # Push buttons to the bottom

        # region Action Buttons
        self.button_frame = ctk.CTkFrame(self, fg_color=TestThemeColors.transparent)
        self.button_frame.grid(
            row=10,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=TestThemeSizes.item_card_element_padding_x,
            pady=(0, TestThemeSizes.item_card_element_padding_y),
        )

        self.button_edit = ctk.CTkButton(
            self.button_frame,
            text="Edit",
            width=310,
            height=32,
            corner_radius=5,
            fg_color=TestThemeColors.text_primary,
            hover_color=TestThemeColors.text_muted,
        )
        self.button_edit.pack(side="left")

        self.button_delete = ctk.CTkButton(
            self.button_frame,
            text="\U0001f5d1",
            width=38,
            height=32,
            corner_radius=5,
            fg_color=TestThemeColors.danger,
            hover_color=TestThemeColors.danger_hover,
        )
        self.button_delete.pack(side="right")
        # endregion


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Item Card Wireframe Test")
    app.geometry("700x500")
    app.minsize(480, 410)

    bg_frame = ctk.CTkFrame(app, fg_color=TestThemeColors.surface)
    bg_frame.pack(fill="both", expand=True)

    wireframe = ItemCardWireframe(bg_frame)
    wireframe.pack(padx=20, pady=20)

    app.mainloop()
