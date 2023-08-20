import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        self.expense_data = []
        self.load_data()

        self.expense_name_label = tk.Label(root, text="Expense Name:")
        self.expense_name_label.pack()
        self.expense_name_entry = tk.Entry(root)
        self.expense_name_entry.pack()

        self.expense_amount_label = tk.Label(root, text="Expense Amount:")
        self.expense_amount_label.pack()
        self.expense_amount_entry = tk.Entry(root)
        self.expense_amount_entry.pack()

        self.expense_date_label = tk.Label(root, text="Expense Date (YYYY-MM-DD):")
        self.expense_date_label.pack()
        self.expense_date_entry = tk.Entry(root)
        self.expense_date_entry.pack()

        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_button.pack()

        self.tree = ttk.Treeview(root, columns=("Date", "Name", "Amount"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Amount", text="Amount")

        self.tree_scroll = tk.Scrollbar(root, command=self.tree.yview)
        self.tree.config(yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.pack(side=tk.LEFT,fill=tk.Y)

        self.tree.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        button_frame = tk.Frame(root)
        button_frame.pack()

        self.display_button = tk.Button(button_frame, text="Display Data", command=self.display_data)
        self.display_button.pack(side="left",padx=10, pady=5)

        self.hide_button = tk.Button(button_frame, text="Hide Data", command=self.hide_data)
        self.hide_button.pack(side="left",padx=10, pady=4)

        bottom_frame = tk.Frame(root)
        bottom_frame.pack()

        self.edit_button = tk.Button(bottom_frame, text="Edit Expense", command=self.edit_expense)
        self.edit_button.pack(side="left",padx=10, pady=3)

        self.delete_button = tk.Button(bottom_frame,bg='red', text="Delete Expense", command=self.delete_expense)
        self.delete_button.pack(side="left",padx=10, pady=2)

        self.total_amount = tk.StringVar()
        self.total_amount_label = tk.Label(root, text="Total Amount:")
        self.total_amount_label.pack()
        self.total_label = tk.Label(root, textvariable=self.total_amount)
        self.total_label.pack()

        self.calculate_total_button = tk.Button(root, text="Calculate Total", command=self.calculate_total)
        self.calculate_total_button.pack()
        
        self.clear_total_button = tk.Button(root, text="Clear Total", command=self.clear_total)
        self.clear_total_button.pack()

        self.sort_by_date_button = tk.Button(root, text="Sort by Date", command=self.sort_by_date)
        self.sort_by_date_button.pack(side="bottom", pady=5)
        

    def add_expense(self):
        name = self.expense_name_entry.get()
        amount = self.expense_amount_entry.get()
        date = self.expense_date_entry.get()

        if name and amount and date:
            try:
                amount = float(amount)
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number.")
                return

            if self.validate_date(date):
                expense = {"date": date, "name": name, "amount": amount}
                self.expense_data.append(expense)
                self.expense_name_entry.delete(0, tk.END)
                self.expense_amount_entry.delete(0, tk.END)
                self.expense_date_entry.delete(0, tk.END)
                self.save_data()
                messagebox.showinfo("Expense Added", "Expense added successfully.")
            else:
                messagebox.showerror("Error", "Invalid date format (YYYY-MM-DD).")
        else:
            messagebox.showerror("Error", "Please enter name, amount, and date.")

    def display_data(self):
        self.tree.delete(*self.tree.get_children())
        for expense in self.expense_data:
            self.tree.insert("", tk.END, values=(expense.get("date"), expense.get("name"), expense.get("amount")))

    def hide_data(self):
        self.tree.delete(*self.tree.get_children())

    def save_data(self):
        with open("expense_data.json", "w") as file:
            json.dump(self.expense_data, file)

    def load_data(self):
        try:
            with open("expense_data.json", "r") as file:
                self.expense_data = json.load(file)
        except FileNotFoundError:
            pass

    def calculate_total(self):
        total = sum(expense["amount"] for expense in self.expense_data)
        self.total_amount.set(f"${total:.2f}")
        
    
    def clear_total(self):
        self.total_amount.set("")
    
    def sort_by_date(self):
        self.expense_data.sort(key=lambda expense: expense["date"])
        self.display_data()
        
    @staticmethod
    def validate_date(date_text):
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def edit_expense(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_item = selected_item[0]
            selected_values = self.tree.item(selected_item, "values")
            if len(selected_values) == 3:
                selected_date, selected_name, selected_amount = selected_values
                self.expense_name_entry.delete(0, tk.END)
                self.expense_name_entry.insert(0, selected_name)
                self.expense_amount_entry.delete(0, tk.END)
                self.expense_amount_entry.insert(0, selected_amount)
                self.expense_date_entry.delete(0, tk.END)
                self.expense_date_entry.insert(0, selected_date)
                self.delete_expense()
        else:
            messagebox.showerror("Error", "Select an expense to edit.")

    def delete_expense(self):
        selected_item = self.tree.selection()
        if selected_item:
            for item in selected_item:
                selected_values = self.tree.item(item, "values")
                if selected_values:
                    selected_name = selected_values[1]
                    self.expense_data = [expense for expense in self.expense_data if expense["name"] != selected_name]
                    self.tree.delete(item)
                    self.save_data()
        else:
            messagebox.showerror("Error", "Select an expense to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
