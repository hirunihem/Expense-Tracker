import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict


# create a csv module to read and write expenses
FILENAME = "expenses.csv"
def initialize_file():
    try:
        with open(FILENAME, 'x', newline='') as file:
            writer= csv.writer(file)
            writer.writerow(['Date', 'Category', 'Amount'])
    except FileExistsError:
        pass

#adding a new expense
def add_expense():
    amount = float(input("Enter amount: "))
    category = input("Enter category (e.g., Food, Travel, Utilities): ")
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")

    if date.strip() == "":
        date = str(datetime.today().date())

    with open(FILENAME, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount])

    print("Expense added successfully!\n")

#view all expenses
def view_expense():
    print("\n All Expenses:\n")
    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            print(f"Date: {row[0]} | Category: {row[1]} | Amount: Rs.{row[2]}")

#show all spending
def show_total():
    total=0
    with open(FILENAME, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            total += float(row[2])
    print(f"\n Total Spending: Rs.{total:2f}\n")

#category filtering
def filter_by_category():
    category = input("Enter category to filter: ").lower()
    total=0
    print(f"\n Expenses in Category '{category}':\n")
    with open(FILENAME, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[1].lower() == category:
                print(f"Date: {row[0]} | Amount: Rs.{row[2]}")
                total += float(row[2])
    print(f"\n Total in '{category}': Rs.{total:2f}\n")

#pie chart
def show_pie_chart():
    category_totals = defaultdict(float)

    try:
        with open(FILENAME, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                category = row[1].lower()
                amount = float(row[2])
                category_totals[category] += amount

        if not category_totals:
            print("No expenses recorded yet.\n")
            return

        categories = list(category_totals.keys())
        amounts = list(category_totals.values())

        plt.figure(figsize=(6, 6))
        plt.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%",
            startangle=140,
            colors=plt.cm.get_cmap('Set3')(range(len(categories)))
        )
        plt.title("Spending by Category")
        plt.axis("equal")
        plt.show()

    except FileNotFoundError:
        print("No data file found. Please add an expense first.\n")


#show menu
def menu():
    while True:
        print("\n_____________Expense Tracker____________")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Total Spending")
        print("4. Filter by Category")
        print("5. Show Spending Pie Chart")
        print("6. Exit")
        choice= input("Choose an option (1-6): ")

        if choice == '1':
            add_expense()
        elif choice =='2':
            view_expense()
        elif choice == '3':
            show_total()
        elif choice == '4':
            filter_by_category()
        elif choice == '5':
            show_pie_chart()
        elif choice == '6':
            print("Exiting. Thank You!")
            break
        else:
            print("Invalid Choice. Please try again.")

#run
initialize_file()
menu()