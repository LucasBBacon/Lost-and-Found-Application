import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import List

from src.database import InventoryManager, Item, ItemStatus


class LostFoundApp:
    """
    Main application window for the Lost and Found application.
    """
    
    def __init__(self, root: tk.Tk, manager: InventoryManager) -> None:
        """
        Initializes the UI.

        Args:
            root (tk.Tk): The root tkinter window.
            manager (InventoryManager): The database controller instance.
        """
        self.manager = manager
        self.root = root
        self.root.title("Lost and Found Manager")
        self.root.geometry("1000x600")
        
        self._setup_styles()
        self._create_header_frame()
        self._create_list_frame()
        self._create_action_frame()
        
    def _setup_styles(self) -> None:
        """
        Configures the ttk styles for the application.
        """
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", rowheight=25)
        style.configure("TButton", padding=6)
        
    def _create_header_frame(self) -> None:
        """
        Creates the top bar with search and filters.
        """
        header = ttk.Frame(self.root, padding="10")
        header.pack(fill=tk.X)
        
        ttk.Label(header, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(header, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(header, text="Go", command=self.perform_search).pack(side=tk.LEFT)
        
        ttk.Frame(header).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(header, text="Filter Status:").pack(side=tk.LEFT, padx=(0, 5))
        self.filter_var = tk.StringVar()
        status_options = ["All"] + [s.value for s in ItemStatus]
        self.filter_combo = ttk.Combobox(header, textvariable=self.filter_var, values=status_options, state="readonly")
        self.filter_combo.current(0)
        self.filter_combo.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(header, text="Apply Filter").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(header, text="Reset", command=self.refresh_list).pack(side=tk.LEFT)
        
    def _create_list_frame(self) -> None:
        """
        Creates a main section of the application with a treeview list.
        """
        list_frame = ttk.Frame(self.root, padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Name", "Category", "Date", "Location", "Status", "Contact")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.column("ID", width=30)
        self.tree.column("Name", width=150)
        self.tree.column("Contact", width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def _create_action_frame(self) -> None:
        """
        Creates the bottom bar with action buttons.
        """
        action_frame = ttk.Frame(self.root, padding="10")
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text="Add new Item", command=self.open_add_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Mark as Claimed", command=self.mark_as_claimed).pack(side=tk.LEFT, padx=5)
        
        ttk.Frame(action_frame).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(action_frame, text="Delete Selected", command=self.delete_item).pack(side=tk.RIGHT, padx=5)
        
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
        
    def perform_filter(self):
        """
        Filters items on the treeview based on status.
        """
        status_str = self.filter_var.get()
        if status_str == "All":
            self.refresh_list()
            return
        
        status_enum = ItemStatus(status_str)
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
        AddWindow(self.root, self.manager, self.refresh_list)
     
        
class AddWindow(tk.Toplevel):
    """
    Popup window for adding a new item.
    """
    def __init__(self, parent, manager, callback):
        super().__init__(parent)
        self.manager = manager
        self.callback = callback
        self.title("Add New Item")
        self.geometry("400x500")
        
        self._create_form()
        
    def _create_form(self):
        """
        Creates the form with relevant input fields.
        """
        form_frame = ttk.Frame(self, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text="Item Name:").pack(anchor=tk.W, pady=(10, 0))
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.pack(fill=tk.X)
        
        ttk.Label(form_frame, text="Category:").pack(anchor=tk.W, pady=(10, 0))
        self.cat_entry = ttk.Entry(form_frame)
        self.cat_entry.pack(fill=tk.X)
        
        ttk.Label(form_frame, text="Date (YYYY-MM-DD):").pack(anchor=tk.W, pady=(10, 0))
        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.pack(fill=tk.X)
        self.date_entry.insert(0, "2025-01-01")
        
        ttk.Label(form_frame, text="Location:").pack(anchor=tk.W, pady=(10, 0))
        self.loc_entry = ttk.Entry(form_frame)
        self.loc_entry.pack(fill=tk.X)
        
        ttk.Label(form_frame, text="Status:").pack(anchor=tk.W, pady=(10, 0))
        self.status_var = tk.StringVar(value=ItemStatus.LOST.value)
        status_options = [s.value for s in ItemStatus]
        self.status_combo = ttk.Combobox(form_frame, textvariable=self.status_var, values=status_options)
        self.status_combo.pack(fill=tk.X)
        
        ttk.Label(form_frame, text="Contact Info:").pack(anchor=tk.W, pady=(10, 0))
        self.contact_entry = ttk.Entry(form_frame)
        self.contact_entry.pack(fill=tk.X)
        
        ttk.Button(form_frame, text="Save Item", command=self.save_item).pack(pady=20, fill=tk.X)
        
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
            messagebox.showinfo("Sucess", "Item added successfully!")
            self.callback()
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
            