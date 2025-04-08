import os
import json
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Arquivo de dados
DATA_FILE = "accounts.json"

# Lista de serviços carregados da base JSON
accounts = []

# --- Funções de manipulação de dados ---
def load_accounts_on_startup():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            accounts.clear()
            for service, data in raw_data.items():
                row = {"Service": service}
                row.update(data)
                accounts.append(row)

def save_accounts_to_file():
    data = {row["Service"]: {
        "username": row["username"],
        "recurring_billing": row["recurring_billing"],
        "payment_method": row["payment_method"],
        "currency": row["currency"]
    } for row in accounts}
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def calculate_totals():
    monthly_usd = 0.0
    monthly_brl = 0.0
    yearly_usd = 0.0
    yearly_brl = 0.0

    for row in accounts:
        currency_str = row.get("currency", "").strip()
        billing = row.get("recurring_billing", "").strip().lower()

        try:
            if currency_str.startswith("R$"):
                val = float(currency_str.replace("R$", "").strip())
                if billing in ["monthly", "mensal"]:
                    monthly_brl += val
                elif billing in ["yearly", "annually", "annual", "anual"]:
                    yearly_brl += val

            elif currency_str.startswith("US$"):
                val = float(currency_str.replace("US$", "").replace(",", "").strip())
                if billing in ["monthly", "mensal"]:
                    monthly_usd += val
                elif billing in ["yearly", "annually", "annual", "anual"]:
                    yearly_usd += val

        except ValueError:
            continue

    return monthly_usd, monthly_brl, yearly_usd, yearly_brl




# --- UI Helpers ---
def refresh_table():
    for item in table.get_children():
        table.delete(item)
    for row in accounts:
        table.insert("", "end", values=[
            row.get("Service", ""),
            row.get("username", ""),
            row.get("recurring_billing", ""),
            row.get("payment_method", ""),
            row.get("currency", "")
        ])

    mu, mb, yu, yb = calculate_totals()

    total_usd_yearly = (mu * 12) + yu
    total_brl_yearly = (mb * 12) + yb

    br_format = lambda v: f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    us_format = lambda v: f"{v:,.2f}"

    totals_label.config(text=(
        f"Mensal → US$: {us_format(mu)}   |   R$: {br_format(mb)}\n"
        f"Anual  → US$: {us_format(yu)}   |   R$: {br_format(yb)}\n"
        f"Total anual equivalente → US$: {us_format(total_usd_yearly)}   |   R$: {br_format(total_brl_yearly)}"
    ))


def get_selected_service():
    selected = table.focus()
    if selected:
        values = table.item(selected, "values")
        return values[0]  # Nome do serviço
    return None

def add_service():
    open_editor_window()

def edit_service():
    service_name = get_selected_service()
    if service_name:
        for row in accounts:
            if row["Service"] == service_name:
                open_editor_window(row)
                break
    else:
        messagebox.showinfo("Editar", "Selecione um serviço para editar.")

def delete_service():
    service_name = get_selected_service()
    if service_name:
        if messagebox.askyesno("Remover", f"Deseja realmente remover '{service_name}'?"):
            global accounts
            accounts = [r for r in accounts if r["Service"] != service_name]
            save_accounts_to_file()
            refresh_table()
    else:
        messagebox.showinfo("Remover", "Selecione um serviço para remover.")

def open_editor_window(data=None):
    win = ttk.Toplevel(root)
    win.title("Editar Serviço" if data else "Novo Serviço")
    win.geometry("400x300")

    fields = {
        "Service": tk.StringVar(value=data["Service"] if data else ""),
        "username": tk.StringVar(value=data.get("username", "") if data else ""),
        "recurring_billing": tk.StringVar(value=data.get("recurring_billing", "") if data else ""),
        "payment_method": tk.StringVar(value=data.get("payment_method", "") if data else ""),
        "currency": tk.StringVar(value=data.get("currency", "") if data else "")
    }

    row = 0
    for label, var in fields.items():
        ttk.Label(win, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=5)
        ttk.Entry(win, textvariable=var).grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1

    def save():
        entry = {k: v.get() for k, v in fields.items()}
        if not entry["Service"]:
            messagebox.showwarning("Erro", "Nome do serviço é obrigatório.")
            return
        # Atualiza ou adiciona
        found = False
        for i, row in enumerate(accounts):
            if row["Service"] == entry["Service"]:
                accounts[i] = entry
                found = True
                break
        if not found:
            accounts.append(entry)
        save_accounts_to_file()
        refresh_table()
        win.destroy()

    ttk.Button(win, text="Salvar", command=save).grid(row=row, column=0, columnspan=2, pady=15)

# --- Interface principal ---
root = ttk.Window(title="Gerenciador de Assinaturas", themename="superhero", size=(850, 550))

columns = ["Service", "username", "recurring_billing", "payment_method", "currency"]
table = ttk.Treeview(root, columns=columns, show="headings", height=15)
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=150)
table.pack(fill="both", expand=True, padx=10, pady=10)

# Botões
frame_btns = ttk.Frame(root)
frame_btns.pack(pady=5)

ttk.Button(frame_btns, text="Adicionar", command=add_service, bootstyle="success").pack(side="left", padx=5)
ttk.Button(frame_btns, text="Editar", command=edit_service, bootstyle="warning").pack(side="left", padx=5)
ttk.Button(frame_btns, text="Remover", command=delete_service, bootstyle="danger").pack(side="left", padx=5)


# Totais
totals_frame = ttk.Frame(root, padding=10, bootstyle="info")  # fundo azul claro
totals_frame.pack(pady=10, fill="x", padx=10)

totals_label = ttk.Label(
    totals_frame,
    text="",
    font=("Segoe UI", 10),
    anchor="center",
    justify="center"
)
totals_label.pack()


# Carrega dados e exibe
load_accounts_on_startup()
refresh_table()

root.mainloop()
