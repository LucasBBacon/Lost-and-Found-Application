from pathlib import Path
from typing import Any

import customtkinter as ctk


class ItemCardWireframe(ctk.CTkFrame):
    def __init__(self, master: Any, **kwargs) -> None:
        super().__init__(master,
                         width=400,
                         height=370,
                         border_color="#cccccc",
                         border_width=1,
                         corner_radius=10,
                         fg_color="#ffffff", 
                         **kwargs)
        self._build_wireframe()
        self.grid_propagate(False)
        
    def _build_wireframe(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.label_name = ctk.CTkLabel(
            self,
            text="Item Name",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.label_name.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        
        self.test_frame = ctk.CTkFrame(self, width=100, height=30, corner_radius=0, fg_color="#000000")
        self.test_frame.grid(row=0, column=1, sticky="e", padx=10)
        
        self.label_status = ctk.CTkLabel(
            self.test_frame,
            text="[Status]",
            font=ctk.CTkFont(weight="bold"),
            anchor="e",
            text_color="#ffffff"
        )
        self.label_status.grid(row=0, column=1, sticky="e", padx=10, pady=(10, 0))

        self.tag_label = ctk.CTkLabel(
            self,
            text="\U0001F3F7",
            font=ctk.CTkFont(size=16),
            text_color="#888888"
        )
        self.tag_label.grid(row=1, column=0, sticky="w", padx=(10, 0))

        self.label_category = ctk.CTkLabel(
            self,
            text="[Category]",
            text_color="#888888",
            font=ctk.CTkFont(size=12)
        )
        self.label_category.grid(row=1, column=0, sticky="w", padx=(30, 10))

        self.label_date_icon = ctk.CTkLabel(
            self,
            text="\U0001F4C5",
            font=ctk.CTkFont(size=18),
            text_color="#000000"
        )
        self.label_date_icon.grid(row=2, column=0, sticky="w", padx=(10, 0), pady=(50, 10))

        self.label_date = ctk.CTkLabel(
            self,
            text="[YYYY-MM-DD]",
            text_color="#000000",
            font=ctk.CTkFont(size=16)
        )
        self.label_date.grid(row=2, column=0, sticky="w", padx=(30, 10), pady=(50, 10))
        

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Item Card Wireframe Test")
    app.geometry("700x500")
    app.minsize(480, 410)
    
    bg_frame = ctk.CTkFrame(app, fg_color="#ffffff")
    bg_frame.pack(fill="both", expand=True)

    wireframe = ItemCardWireframe(bg_frame)
    wireframe.pack(padx=20, pady=20)

    app.mainloop()