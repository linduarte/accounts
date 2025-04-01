import tkinter as tk
from tkinter import ttk, messagebox
import json

DATA_FILE = "accounts.json"

def load_accounts():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_accounts(accounts):
    with open(DATA_FILE, "w") as file:
        json.dump(accounts, file, indent=4)

def add_account():
    service = entry_service.get().strip()
    username = entry_username.get().strip()
    billing = entry_billing.get().strip()
    payment = entry_payment.get().strip()
    currency = entry_currency.get().strip()
    
    if not service or not username:
        messagebox.showwarning("Input Error", "Service name and username are required!")
        return
    
    accounts[service] = {
        "username": username,
        "recurring_billing": billing,
        "payment_method": payment,
        "currency": currency
    }
    save_accounts(accounts)
    refresh_table()
    clear_entries()

def edit_account():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "No account selected!")
        return
    
    service = tree.item(selected_item, "values")[0]
    username = entry_username.get().strip()
    billing = entry_billing.get().strip()
    payment = entry_payment.get().strip()
    currency = entry_currency.get().strip()
    
    if not username:
        messagebox.showwarning("Input Error", "Username cannot be empty!")
        return
    
    accounts[service] = {
        "username": username,
        "recurring_billing": billing,
        "payment_method": payment,
        "currency": currency
    }
    save_accounts(accounts)
    refresh_table()

def delete_account():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "No account selected!")
        return
    
    service = tree.item(selected_item, "values")[0]
    del accounts[service]
    save_accounts(accounts)
    refresh_table()

def refresh_table():
    tree.delete(*tree.get_children())
    for service, details in accounts.items():
        tree.insert("", "end", values=(service, details["username"], details["recurring_billing"], details["payment_method"], details["currency"]))

def clear_entries():
    entry_service.delete(0, tk.END)
    entry_username.delete(0, tk.END)
    entry_billing.delete(0, tk.END)
    entry_payment.delete(0, tk.END)
    entry_currency.delete(0, tk.END)

# Load data
tk_root = tk.Tk()
tk_root.title("Account Manager")
tk_root.geometry("600x400")
accounts = load_accounts()

frame = tk.Frame(tk_root)
frame.pack(pady=10)

# Form Fields
tk.Label(frame, text="Service").grid(row=0, column=0)
entry_service = tk.Entry(frame)
entry_service.grid(row=0, column=1)

tk.Label(frame, text="Username").grid(row=1, column=0)
entry_username = tk.Entry(frame)
entry_username.grid(row=1, column=1)

tk.Label(frame, text="Billing").grid(row=2, column=0)
entry_billing = tk.Entry(frame)
entry_billing.grid(row=2, column=1)

tk.Label(frame, text="Payment").grid(row=3, column=0)
entry_payment = tk.Entry(frame)
entry_payment.grid(row=3, column=1)

tk.Label(frame, text="Currency").grid(row=4, column=0)
entry_currency = tk.Entry(frame)
entry_currency.grid(row=4, column=1)

# Buttons
tk.Button(frame, text="Add", command=add_account).grid(row=5, column=0, pady=10)
tk.Button(frame, text="Edit", command=edit_account).grid(row=5, column=1)
tk.Button(frame, text="Delete", command=delete_account).grid(row=5, column=2)

# Table (Treeview)
tree = ttk.Treeview(tk_root, columns=("Service", "Username", "Billing", "Payment", "Currency"), show="headings")
for col in ("Service", "Username", "Billing", "Payment", "Currency"):
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(pady=10)
refresh_table()

tk_root.mainloop()
