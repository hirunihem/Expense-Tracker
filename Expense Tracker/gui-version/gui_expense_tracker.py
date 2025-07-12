import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

FILENAME = "expenses.csv"

# Step 1: Initialize the CSV file
def initialize_file():
    try:
        with open(FILENAME, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount"])
    except FileExistsError:
        pass

# Step 2: Save a new expense
def save_expense():
    date = date_entry.get() or str(datetime.today().date())
    category = category_entry.get()
    amount = amount_entry.get()

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")
        return

    if not category.strip():
        messagebox.showerror("Error", "Category is required.")
        return

    with open(FILENAME, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount])

    messagebox.showinfo("Success", "Expense added.")
    clear_inputs()
    refresh_table()

# Step 3: Refresh table and total
def refresh_table():
    for row in expense_table.get_children():
        expense_table.delete(row)

    total = 0
    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            expense_table.insert("", tk.END, values=row)
            total += float(row[2])

    total_label.config(text=f"Total Spending: Rs.{total:.2f}")

# Step 4: Clear inputs
def clear_inputs():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

# Step 5: Filter by category
def filter_by_category():
    category = category_entry.get().strip().lower()
    if not category:
        messagebox.showinfo("Info", "Please enter a category to filter.")
        return

    for row in expense_table.get_children():
        expense_table.delete(row)

    total = 0
    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[1].lower() == category:
                expense_table.insert("", tk.END, values=row)
                total += float(row[2])

    total_label.config(text=f"Total in '{category}': Rs.{total:.2f}")

# Step 6: Show pie chart
def show_pie_chart():
    category_totals = defaultdict(float)

    try:
        with open(FILENAME, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                category = row[1].strip().lower()
                amount = float(row[2])
                category_totals[category] += amount

        if not category_totals:
            messagebox.showinfo("Info", "No data to plot.")
            return

        categories = list(category_totals.keys())
        amounts = list(category_totals.values())

        plt.figure(figsize=(6, 6))
        cmap = plt.get_cmap('Set3')
        colors = cmap(range(len(categories)))
        plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140, colors=colors)
        plt.title("Spending by Category")
        plt.axis("equal")
        plt.show()

    except FileNotFoundError:
        messagebox.showerror("Error", "CSV file not found.")

# ============ GUI Setup ============

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x550")
root.configure(bg='#ABDBFC')

# Input Fields
tk.Label(root, bg='#ABDBFC', text="Date (YYYY-MM-DD):").pack()
date_entry = tk.Entry(root, bg="#C4F6E3")
date_entry.pack()

tk.Label(root, bg='#ABDBFC', text="Category:").pack()
category_entry = tk.Entry(root, bg="#C4F6E3")
category_entry.pack()

tk.Label(root, bg='#ABDBFC', text="Amount:").pack()
amount_entry = tk.Entry(root, bg="#C4F6E3")
amount_entry.pack()

# Buttons
tk.Button(root, bg="#3BDDA2", activebackground="#b3d9ff", text="Add Expense", command=save_expense).pack(pady=5)
tk.Button(root, bg="#3BDDA2", activebackground="#b3d9ff", text="Filter by Category", command=filter_by_category).pack(pady=5)
tk.Button(root, bg="#3BDDA2", activebackground="#b3d9ff", text="Show Pie Chart", command=show_pie_chart).pack(pady=5)

# Expense Table
expense_table = ttk.Treeview(root, columns=("Date", "Category", "Amount"), show="headings")
expense_table.heading("Date", text="Date")
expense_table.heading("Category", text="Category")
expense_table.heading("Amount", text="Amount")
expense_table.pack(pady=10, fill="both", expand=True)

# Total Label
total_label = tk.Label(root, text="Total Spending: Rs.0.00", font=("Arial", 12, "bold"))
total_label.pack(pady=10,)

# Initialize and run
initialize_file()
refresh_table()
root.mainloop()
