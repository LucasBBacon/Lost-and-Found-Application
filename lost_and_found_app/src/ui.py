import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk 
from typing import List

from src.database import InventoryManager, Item, ItemStatus


class LostFoundApp(ctk.CTk):
    """
    Main application window for the Lost and Found application.
    """
    
    def __init__(self, root, manager: InventoryManager) -> None:
        """
        Initializes the UI.

        Args:
            root (tk.Tk): The root tkinter window.
            manager (InventoryManager): The database controller instance.
        """
        super().__init__()
        
        self.manager = manager
        self.title("Lost and Found Manager")
        self.geometry("1000x700")
        
        self.current_mode = "System"
        
        self._setup_menubar()
        self._create_layout()
        
        self.refresh_list()
        
        self._apply_treeview_style()
        
    def _setup_menubar(self) -> None:
        menubar = tk.Menu(self)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Add New Item", command=self.open_add_window)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Mark as Claimed", command=self.mark_as_claimed)
        edit_menu.add_command(label="Delete Selected", command=self.delete_item)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Toggle Theme (Light/Dark)", command=self.toggle_theme)
        view_menu.add_command(label="Refresh List", command=self.refresh_list)
        menubar.add_cascade(label="View", menu=view_menu)
        
        self.config(menu=menubar)
    
    def _create_layout(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.header = ctk.CTkFrame(self, corner_radius=10)
        self.header.grid(row=0, column=0, sticky='ew', padx=15, pady=10)
        self._build_header_widgets()
        
        self.list_frame = ctk.CTkFrame(self, corner_radius=10)
        self.list_frame.grid(row=1, column=0, sticky='nsew', padx=15, pady=5)
        self._build_list_widgets()
        
        self.action_frame = ctk.CTkFrame(self, corner_radius=10)
        self.action_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=10)
        self._build_action_widgets()
    
    def _build_header_widgets(self) -> None:
        """
        Creates the top bar with search and filters.
        """
        ctk.CTkLabel(self.header, text="Search:").pack(side=tk.LEFT, padx=(15, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(self.header, textvariable=self.search_var, width=200, placeholder_text="Keyword...")
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(self.header, text="Go", width=60, command=self.perform_search).pack(side=tk.LEFT, padx=5)
        
        ctk.CTkLabel(self.header, text="Filter Status:").pack(side=tk.LEFT, padx=(20, 5))
        status_options = ["All"] + [s.value for s in ItemStatus]
        self.filter_combo = ctk.CTkComboBox(self.header, values=status_options, command=self.perform_filter)
        self.filter_combo.set("All")
        self.filter_combo.pack(side=tk.LEFT, padx=5)
        
        self.theme_switch = ctk.CTkSwitch(self.header, text = "Dark Mode", command=self.toggle_theme_switch)
        self.theme_switch.pack(side=tk.RIGHT, padx=15)
        self.theme_switch.select()
        
    def _build_list_widgets(self) -> None:
        """
        Creates a main section of the application with a treeview list.
        """
        
        columns = ("ID", "Name", "Category", "Date", "Location", "Status", "Contact")
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Name", width=180)
        self.tree.column("Contact", width=180)
        
        scrollbar = ctk.CTkScrollbar(self.list_frame, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        
    def _build_action_widgets(self) -> None:
        """
        Creates the bottom bar with action buttons.
        """
        ctk.CTkButton(self.action_frame, text="Add new Item", command=self.open_add_window).pack(side=tk.LEFT, padx=15, pady=15)
        ctk.CTkButton(self.action_frame, text="Mark as Claimed", fg_color="green", command=self.mark_as_claimed).pack(side=tk.LEFT, padx=5, pady=15)
        
        ctk.CTkButton(self.action_frame, text="Delete Selected", fg_color="#C62828", hover_color="#B71C1C", command=self.delete_item).pack(side=tk.RIGHT, padx=15, pady=15)
        
    def _apply_treeview_style(self):
        mode = ctk.get_appearance_mode()
        style = ttk.Style()
        style.theme_use('clam')
        
        if mode == "Dark":
            bg_colour = "#2b2b2b"
            text_colour = "white"
            field_bg = "#2b2b2b"
            header_bg = "#1f1f1f"
        else:
            bg_colour = "white"
            text_colour = "black"
            field_bg = "white"
            header_bg = "#e1e1e1"
            
        style.configure("Treeview",
                        background=bg_colour,
                        foreground=text_colour,
                        fieldbackground=field_bg,
                        borderwidth=0,
                        font=('Arial', 11))
        
        style.configure("Treeview.Heading",
                        background=header_bg,
                        foreground=text_colour,
                        font=('Arial', 11, 'bold'))
        
        style.map('Treeview', background=[('selected', '#1f538d')])
        
    def toggle_theme_switch(self) -> None:
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")
        self._apply_treeview_style()
    
    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        new_mode = "Light" if current == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        
        if new_mode == "Dark":
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()
            
        self._apply_treeview_style()
    
    def refresh_list(self):
        """
        Clears and reloads the list with all items.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        items = self.manager.get_all_items()
        for item in items:
            self.tree.insert("", tk.END, values=(
                item.id, 
                item.name, 
                item.category, 
                item.date_lost, 
                item.location, 
                item.status.value, 
                item.contact_info
            ))
            
    def perform_search(self):
        """
        Searches items in the database based on a keyword.
        """
        keyword = self.search_var.get()
        if not keyword:
            return
        
        results = self.manager.search_items(keyword)
        self._update_tree_with_results(results)
        
    def perform_filter(self, choice: str):
        """
        Filters items on the treeview based on status.
        """
        if choice == "All":
            self.refresh_list()
        else:
            status_enum = ItemStatus(choice)
            results = self.manager.filter_by_status(status_enum)
            self._update_tree_with_results(results)
        
    def _update_tree_with_results(self, items: List[Item]):
        """
        Helper to update main treeview with a specific list of items.

        Args:
            items (_type_): List of items to populate the treeview.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in items:
            self.tree.insert("", tk.END, values=(
                item.id, 
                item.name, 
                item.category, 
                item.date_lost, 
                item.location, 
                item.status.value, 
                item.contact_info
            ))
            
    def mark_as_claimed(self):
        """
        Updates the selected item's status to Claimed.
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item first.")
            return
        
        item_values = self.tree.item(selected[0])['values']
        item_id = item_values[0]
        
        self.manager.update_item_status(int(item_id), ItemStatus.CLAIMED)
        self.refresh_list()
        messagebox.showinfo("Success", "Item marked as Claimed.")
        
    def delete_item(self):
        """
        Deletes the selected item.
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item first.")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this item?"):
            return
        
        item_values = self.tree.item(selected[0])["values"]
        item_id = item_values[0]
        
        self.manager.delete_item(int(item_id))
        self.refresh_list()
        
        
    def open_add_window(self):
        """
        Opens a popup window to add a new item.
        """
        AddWindow(self, self.manager, self.refresh_list)
     
        
class AddWindow(ctk.CTkToplevel):
    """
    Popup window for adding a new item.
    """
    def __init__(self, parent, manager, callback):
        super().__init__(parent)
        self.manager = manager
        self.callback = callback
        self.title("Add New Item")
        self.geometry("400x500")
        
        self.transient(parent)
        self.lift()
        
        self._create_form()
        
    def _create_form(self):
        """
        Creates the form with relevant input fields.
        """
        container = ctk.CTkFrame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        def add_field(label_text, row) -> ctk.CTkEntry:
            ctk.CTkLabel(container, text=label_text).grid(row=row, column=0, sticky="w", pady=(10,0))
            entry = ctk.CTkEntry(container, width=250)
            entry.grid(row=row+1, column=0, sticky="ew", pady=(0,5))
            return entry
                    
        self.name_entry = add_field("Item Name:", 0)
        self.cat_entry = add_field("Category:", 2)
        self.date_entry = add_field("Date (YYYY-MM-DD):", 4)
        self.date_entry.insert(0, "2026-01-01")
        self.loc_entry = add_field("Location:", 6)
        
        ctk.CTkLabel(container, text="Status:").grid(row=8, column=0, stick="w", pady=(10,0))
        self.status_var = tk.StringVar(value=ItemStatus.LOST.value)
        status_options = [s.value for s in ItemStatus]
        self.status_combo = ctk.CTkComboBox(container, variable=self.status_var, values=status_options)
        self.status_combo.grid(row=9, column=0, sticky="ew")
        
        self.contact_entry = add_field("Contact Info:", 10)
        
        ctk.CTkButton(container, text="Save Item", command=self.save_item).grid(row=12, column=0, pady=30, sticky="ew")
        
    def save_item(self):
        """
        Attempts to save item and validates the entries.
        """
        try:
            item = Item(name=self.name_entry.get(),
                        category=self.cat_entry.get(),
                        date_lost=self.date_entry.get(),
                        location=self.loc_entry.get(),
                        status=ItemStatus(self.status_var.get()),
                        contact_info=self.contact_entry.get())
            
            self.manager.add_item(item)
            self.callback()
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
            