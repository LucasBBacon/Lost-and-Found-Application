import customtkinter as ctk

class ConfirmDelteModal(ctk.CTkToplevel):
    def __init__(self, parent, item_name, on_confirm):
        super().__init__(parent)
        self.on_confirm = on_confirm
        
        self.title("Confirm Delete")
        self.geometry("300 x 150")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        label = ctk.CTkLabel(self,
                             text=f"Are you sure you want to\ndelete '{item_name}'?",
                             font=("Arial", 14), justify="center")
        label.pack(pady=20, padx=20)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", width=80,
                                   fg_color="transparent", border_width=1,
                                   text_color=("gray10", "gray90"),
                                   command=self.destroy)
        cancel_btn.pack(side="left", padx=10)
        
        delete_btn = ctk.CTkButton(btn_frame, text="Delete", width=80,
                                   fg_color="#d32f2f", hover_color="#b71c1c",
                                   command=self.confirm_action)
        delete_btn.pack(side="left", padx=10)
        
    def confirm_action(self):
        self.on_confirm()
        self.destroy()


class InteractiveRow(ctk.CTkFrame):
    def __init__(self, master, item_text, command, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.item_text = item_text
        self.command = command
        
        self.default_color = ("#f0f0f0", "#2b2b2b")
        self.hover_color = ("#ebebeb", "#3e3e3e")
        self.configure(fg_color=self.default_color, corner_radius=10)
        
        self.label = ctk.CTkLabel(self, text=item_text, anchor="w", font=('Arial', 14))
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.option_menu = ctk.CTkOptionMenu(
            self, values=["Yes", "No", "Maybe"],
            command=self.menu_callback,
            width=80, height=28,
            corner_radius=8,
            fg_color=self.default_color, 
            button_color=self.default_color,
            text_color=("gray10", "gray90"), 
            button_hover_color=("gray75", "gray40"),
            dropdown_fg_color=("white", "gray20")
        )
        self.option_menu.set("Maybe")
        self.option_menu.grid(row=0, column=1, padx=(5, 5), pady=10)
        
        self.delete_btn = ctk.CTkButton(self,
                                        text="x", width=30, height=30,
                                        fg_color=self.default_color,
                                        hover_color=("gray80", "gray25"),
                                        text_color=self.default_color,
                                        state="disabled",
                                        command=self.ask_delete)
        self.delete_btn.grid(row=0, column=2, padx=(0, 10), pady=10)
        
        for widget in [self, self.label, self.option_menu, self.delete_btn]:
            widget.bind("<Enter>", self.on_enter)
            widget.bind("<Leave>", self.on_leave)
    
    def menu_callback(self, choice):
        print(f"Item '{self.item_text}' set to: {choice}")
        
    def ask_delete(self):
        ConfirmDelteModal(self.winfo_toplevel(), self.item_text, self.perform_delete)
    
    def perform_delete(self):
        self.destroy()
    
    def on_enter(self, event):
        self.configure(fg_color=self.hover_color)
        self.delete_btn.configure(text_color="#c62828", state="normal")
        
    def on_leave(self, event):
        self.configure(fg_color=self.default_color)
        self.delete_btn.configure(text_color=("#f0f0f0", "#2b2b2b"), state="disabled")


class ScrollableLabelButtonFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.command = command
        
    def add_item(self, item_text):
        row = InteractiveRow(self, item_text=item_text, command=self.command)
        row.grid(row=len(self.winfo_children()), column=0, sticky="ew", padx=10, pady=(0, 10))
        
    def remove_item(self, item_name):
        pass
    
        
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x500")
        self.title("Custom List with Buttons")
        
        title = ctk.CTkLabel(self, text="Items", font=("Arial", 20, "bold"))
        title.pack(pady=20)
        
        self.scrollable_list = ScrollableLabelButtonFrame(self, width=350, height=500, command=self.button_click_action)
        self.scrollable_list.pack(fill="both", expand=True)
        
        for i in range(20):
            self.scrollable_list.add_item(f"Item Number {i}")
            
    def button_click_action(self, item_text):
        print(f"You clicked the button for: {item_text}")   
    

if __name__ == "__main__":
    app = App()
    app.mainloop()