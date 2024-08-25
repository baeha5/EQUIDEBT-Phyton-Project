import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from PIL import ImageTk, Image


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.group = Group()

    def __str__(self):
        return f"{self.description} - RM{self.amount:.2f}"


class Group:
    def __init__(self):
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def delete_expense_by_description(self, description):
        self.expenses = [expense for expense in self.expenses if str(expense) != description]

    def calculate_balances(self):
        balances = {}
        for expense in self.expenses:
            total_people = len(expense.split_details) + 1
            amount_per_person = expense.amount / total_people

            for person in expense.split_details:
                if person not in balances:
                    balances[person] = 0

                if person == expense.paid_by:
                    balances[person] -= expense.amount
                else:
                    balances[person] += amount_per_person

        return balances


class PersonList:
    def __init__(self, parent_frame):
        self.people_frame = ttk.Frame(parent_frame, style="Custom.TFrame")
        self.people_frame.grid(row=0, column=0, padx=10, pady=10)

        # Set column weights to center the elements
        self.people_frame.columnconfigure(0, weight=3, uniform='a')
        self.people_frame.columnconfigure(1, weight=3, uniform='a')
        self.people_frame.columnconfigure(2, weight=3, uniform='a')

        ttk.Label(self.people_frame, font=("Comic Sans MS", 15), text="People:", style="Custom.TLabel").grid(row=0,
                                                                                                             column=2,
                                                                                                             columnspan=3,
                                                                                                             pady=10)

        # Adjust the column for Listbox, Entry, and Button
        self.people_listbox = tk.Listbox(self.people_frame, selectmode=tk.SINGLE, font=("Comic Sans MS", 10))
        self.people_listbox.grid(row=1, column=2, pady=5, padx=10, sticky="nsew")

        self.people_entry = ttk.Entry(self.people_frame, font=("Comic Sans MS", 10))
        self.people_entry.grid(row=2, column=2, pady=5, padx=5, sticky="nsew")

        ttk.Button(self.people_frame, text="Add Person", command=self.add_person, style="TButton").grid(row=3, column=2,
                                                                                                        pady=10,
                                                                                                        padx=10,
                                                                                                        sticky="nsew")

        self.people = []

    def add_person(self):
        person = self.people_entry.get()
        if person:
            self.people_listbox.insert(tk.END, person)
            self.people_entry.delete(0, tk.END)

    def get_people(self):
        return list(self.people_listbox.get(0, tk.END))


class Authentication:
    def __init__(self):
        self.users = {}

    def register_user(self, username, password):
        if username not in self.users:
            self.users[username] = User(username, password)
            return True
        return False


def authenticate_user(self, username, password):
    user = self.users.get(username)
    if user and user.password == password:
        return user
    return None


class LoginRegisterWindow:
    def __init__(self, root, authentication, on_successful_login):
        self.root = root
        self.authentication = authentication
        self.on_successful_login = on_successful_login

        ttk.Label(root, text="WELCOME TO EQUIDEBT", style="Custom.TLabel", font=("Comic Sans MS", 20)).grid(row=0,
                                                                                                            column=1,
                                                                                                            padx=10,
                                                                                                            pady=10,
                                                                                                            sticky="nsew")

        self.login_register_frame = ttk.Frame(root, style="Custom.TFrame", width=700, height=500)
        self.login_register_frame.grid(row=3, column=2, pady=60, padx=10)

        ttk.Label(self.login_register_frame, text="Username:", font=("Comic Sans MS", 10)).grid(row=0, column=0,
                                                                                                pady=20, padx=5,
                                                                                                sticky="e")
        self.username_entry = ttk.Entry(self.login_register_frame)
        self.username_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.login_register_frame, text="Password:", font=("Comic Sans MS", 10)).grid(row=1, column=0,
                                                                                                pady=25, padx=5,
                                                                                                sticky="e")
        self.password_entry = ttk.Entry(self.login_register_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        ttk.Button(self.login_register_frame, text="Login", command=self.login).grid(row=3, column=1, pady=10)
        ttk.Button(self.login_register_frame, text="Register", command=self.register).grid(row=2, column=1, pady=10)

        # Center the frame
        self.center_frame()

    def center_frame(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        frame_width = 1000  # Adjust this value based on your frame's width
        frame_height = 600  # Adjust this value based on your frame's height

        x = (screen_width - frame_width) // 2
        y = (screen_height - frame_height) // 2

        self.root.geometry(f"{frame_width}x{frame_height}+{x}+{y}")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.authentication.authenticate_user(username, password)

        if user:
            self.on_successful_login(user)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.authentication.register_user(username, password):
            messagebox.showinfo("Success", "Registration successful. You can now log in.")
        else:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")


class ExpenseApp:
    def __init__(self, parent_frame, person_listbox, current_user):
        self.expenses_list = []
        self.parent_frame = parent_frame
        self.person_listbox = person_listbox
        self.current_user = current_user

        notebook = ttk.Notebook(parent_frame, style="Custom.TFrame")
        notebook.grid(row=1, column=0, columnspan=2, pady=10)

        # Person List Tab
        person_list_tab = ttk.Frame(notebook, style="Custom.TFrame")
        notebook.add(person_list_tab, text="Person List")
        self.person_list = PersonList(person_list_tab)

        # Expense Details Tab
        expense_details_tab = ttk.Frame(notebook, style="Custom.TFrame")
        notebook.add(expense_details_tab, text="Expense Details")
        self.setup_expense_details_tab(expense_details_tab)

        # View Balances Tab
        view_balances_tab = ttk.Frame(notebook, style="Custom.TFrame")
        notebook.add(view_balances_tab, text="View Balances")
        self.setup_view_balances_tab(view_balances_tab)

        self.group = Group()

        # Expense tracker tab
        expense_tracker_tab = ttk.Frame(notebook, style="Custom.TFrame")
        notebook.add(expense_tracker_tab, text="Expense tracker")
        self.setup_expense_tracker_tab(expense_tracker_tab)

    def setup_expense_details_tab(self, frame):
        # Configure columns to have equal weight
        frame.columnconfigure(0, weight=1, uniform='a')
        frame.columnconfigure(1, weight=1, uniform='a')
        frame.columnconfigure(2, weight=1, uniform='a')

        ttk.Label(frame, font=("Comic Sans MS", 15), text="Enter expense details:", style="Custom.TLabel").grid(row=0,
                                                                                                                column=0,
                                                                                                                columnspan=3,
                                                                                                                pady=10)

        ttk.Label(frame, text="Description:", style="Custom.TLabel").grid(row=1, column=0, columnspan=2, padx=5)
        self.description_entry = ttk.Entry(frame, font=("Comic Sans MS", 10))
        self.description_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Amount (RM):", style="Custom.TLabel").grid(row=2, column=0, columnspan=2, padx=5)
        self.amount_entry = ttk.Entry(frame, font=("Comic Sans MS", 10))
        self.amount_entry.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Paid by:", style="Custom.TLabel").grid(row=3, column=0, columnspan=2, padx=5)
        self.paid_by_var = tk.StringVar()
        self.paid_by = ttk.Combobox(frame, textvariable=self.paid_by_var, values=self.person_list.get_people(),
                                    font=("Comic Sans MS", 10))
        self.paid_by.grid(row=3, column=1, pady=5)

        self.paid_by.bind("<<ComboboxSelected>>", lambda event: self.update_split_options(event))

        ttk.Label(frame, text="Split by:", style="Custom.TLabel").grid(row=4, column=0, columnspan=2, padx=5)

        self.split_options = ["Equally", "Unequally"]
        self.split_var = tk.StringVar()
        self.split_var.set(self.split_options[0])
        self.split_dropdown = ttk.Combobox(frame, textvariable=self.split_var, values=self.split_options,
                                           font=("Comic Sans MS", 10))
        self.split_dropdown.grid(row=4, column=1, pady=5)

        self.split_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_split_options(event))

        self.split_options_frame = ttk.Frame(frame, style="Custom.TFrame")
        self.split_options_frame.grid(row=5, column=0, columnspan=3)

        self.expenses_text = tk.Text(frame, height=10, width=30, font=("Comic Sans MS", 10))
        self.expenses_text.grid(row=6, column=0, columnspan=3, pady=10)

        self.buttons_frame = ttk.Frame(frame, style="Custom.TFrame")
        self.buttons_frame.grid(row=7, column=0, columnspan=3, pady=10)

        ttk.Button(self.buttons_frame, text="Add Expense", command=self.add_expense, style="TButton").grid(row=0,
                                                                                                           column=0,
                                                                                                           padx=5)
        ttk.Button(self.buttons_frame, text="Reset Details", command=self.reset_details, style="TButton").grid(row=0,
                                                                                                               column=1,
                                                                                                               padx=5)

    def setup_view_balances_tab(self, frame):
        frame.columnconfigure(0, weight=1, uniform='a')
        ttk.Label(frame, font=("Comic Sans MS", 15), text="Balances:", style="Custom.TLabel").grid(row=0, column=0,
                                                                                                   pady=10)

        self.balances_text = tk.Text(frame, height=20, width=30, font=("Comic Sans MS", 10))
        self.balances_text.grid(row=1, column=0, pady=5)

        ttk.Button(frame, text="Calculate Balances", command=self.calculate_and_display_balances, style="TButton").grid(
            row=2, column=0, pady=10)

    def update_split_options(self, event):
        selected_option = self.split_var.get()

        # Destroy only Entry widgets, not other widgets
        for widget in self.split_options_frame.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.destroy()

        ttk.Label(self.split_options_frame, text="Split by:", background="#81DAF5", font=("Comic Sans MS", 10)).grid(
            row=0, column=0, sticky="E", pady=5)

        # Add new label
        ttk.Label(self.split_options_frame, text="Split by:", background="#81DAF5", font=("Comic Sans MS", 10)).grid(
            row=0, column=0, sticky="E", pady=5)

        if selected_option == "Equally":
            # Initialize checkbox_vars
            self.checkbox_vars = [tk.BooleanVar() for _ in range(len(self.person_list.get_people()))]

            # Create Checkbuttons for each person
            for i, person in enumerate(self.person_list.get_people()):
                ttk.Checkbutton(self.split_options_frame, text=person, variable=self.checkbox_vars[i],
                                style="TCheckbutton").grid(row=i + 1, column=0, pady=5)


        elif selected_option == "Unequally":
            # Initialize amount_entries
            self.amount_entries = []

            # Create Labels and Entry widgets for each person
            for i, person in enumerate(self.person_list.get_people()):
                ttk.Label(self.split_options_frame, text=person, background="#FFFFFF", font=("Comic Sans MS", 10)).grid(
                    row=i + 1, column=0, sticky="E", pady=5)
                entry_var = tk.DoubleVar()
                ttk.Entry(self.split_options_frame, textvariable=entry_var, font=("Comic Sans MS", 10)).grid(row=i + 1,
                                                                                                             column=1,
                                                                                                             pady=5)
                self.amount_entries.append(entry_var)

    def add_expense(self):
        selected_option = self.split_var.get()

        if selected_option == "Equally":
            selected_people = [person for person, var in zip(self.person_list.get_people(), self.checkbox_vars) if
                               var.get()]
        elif selected_option == "Unequally":
            amounts = [entry_var.get() for entry_var in self.amount_entries if hasattr(entry_var, 'get')]
            selected_people = list(zip(self.person_list.get_people(), amounts))

        description = self.description_entry.get()
        amount = self.amount_entry.get()
        paid_by = self.paid_by_var.get()

        # Get current date and time in the desired format
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        expense_info_str = self.get_expense_info_str(description, amount, paid_by, selected_option, selected_people)

        expense_info = {"description": description, "amount": amount, "paid_by": paid_by,
                        "split_method": selected_option, "split_details": selected_people, "date_time": date_time}

        self.expenses_list.append(expense_info)
        self.expenses_text.insert(tk.END, self.get_expense_info_str(description, amount, paid_by, selected_option,
                                                                    selected_people) + "\n")

        # Update the Treeview in the Expense Tracker tab
        self.update_expense_tracker_treeview()

    def update_expense_tracker_treeview(self):
        # Assuming self.expense_treeview is the reference to your Treeview widget
        # Clear existing items in the Treeview
        for item in self.expense_treeview.get_children():
            self.expense_treeview.delete(item)

        # Iterate through the expenses_list and insert each expense into the Treeview
        for expense_info in self.expenses_list:
            self.expense_treeview.insert("", tk.END, values=(
                expense_info.get("description", ""),
                expense_info.get("amount", ""),
                expense_info.get("paid_by", ""),
                expense_info.get("split_method", ""),
                expense_info.get("date_time", "")  # Use "date_time" from expense_info
            ))

    def reset_details(self):
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.paid_by_var.set('')
        self.split_var.set(self.split_options[0])

        for widget in self.split_options_frame.winfo_children():
            widget.destroy()

        # Reset the checkbox_vars and amount_entries if they exist
        if hasattr(self, 'checkbox_vars'):
            del self.checkbox_vars
        if hasattr(self, 'amount_entries'):
            del self.amount_entries

        ttk.Label(self.split_options_frame, text="Split by:", background="#81DAF5", font=("Comic Sans MS", 10)).grid(
            row=0, column=0, sticky="E", pady=5)

    def calculate_and_display_balances(self):
        # Assuming you have a tkinter GUI and a text widget named self.balances_text
        self.balances_text.delete(1.0, tk.END)

        # Calculate individual expenses
        individual_expenses = {}
        for expense in self.expenses_list:
            if expense['split_method'] == 'Equally':
                amount_per_person = float(expense['amount']) / len(expense['split_details'])
                for person in expense['split_details']:
                    if person not in individual_expenses:
                        individual_expenses[person] = 0.0
                    individual_expenses[person] += amount_per_person
            elif expense['split_method'] == 'Unequally':
                for person, amount in expense['split_details']:
                    if person not in individual_expenses:
                        individual_expenses[person] = 0.0
                    individual_expenses[person] += amount

        # Display individual expenses
        self.balances_text.insert(tk.END, "The calculated individual expenses are:\n")
        for person, expense in individual_expenses.items():
            self.balances_text.insert(tk.END, f"{person}: RM {expense:.2f}\n")

        # Calculate and display balances
        self.balances_text.insert(tk.END, "\nNow, let's look at the balances:\n")
        owes_dict = {person: 0.0 for person in individual_expenses.keys()}

        for person1, expense1 in individual_expenses.items():
            for person2, expense2 in individual_expenses.items():
                if person1 != person2:
                    debt = expense2 - expense1
                    if debt > 0:
                        owes_dict[person2] += debt

        # Display owes for each person
        for person, amount in owes_dict.items():
            self.balances_text.insert(tk.END, f"{person} owes: RM {amount:.2f}\n")

    def get_expense_info_str(self, description, amount, paid_by, selected_option, selected_people):
        if selected_option == "Equally":
            return f"{description}: RM {amount}, Equally Split Among: {', '.join(selected_people)}"
        elif selected_option == "Unequally":
            return f"{description}: RM {amount}, Unequally Split Among: {', '.join([f'{person} ({amt})' for person, amt in selected_people])}"

    def get_expense_info_str(self, description, amount, paid_by, selected_option, selected_people):
        if selected_option == "Equally":
            return f"{description}: RM {amount}, Equally Split Among: {', '.join(selected_people)}"
        elif selected_option == "Unequally":
            return f"{description}: RM {amount}, Unequally Split Among: {', '.join([f'{person} ({amt})' for person, amt in selected_people])}"

    def setup_expense_tracker_tab(self, frame):
        ttk.Label(frame, text="Expense History:", style="Custom.TLabel").grid(row=0, column=0, pady=10)

        # Expense History Treeview
        columns = ("Description", "Amount", "Paid By", "Split Method", "Date and Time")
        self.expense_treeview = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.expense_treeview.heading(col, text=col)
        self.expense_treeview.grid(row=2, column=0, pady=5)

        ttk.Button(frame, text="Add Expense", command=self.add_expense_to_tracker, style="TButton").grid(row=3,
                                                                                                         column=0,
                                                                                                         pady=10)

    def add_expense_to_tracker(self):
        # Get information from the Expense Details Tab
        selected_option = self.split_var.get()

        if selected_option == "Equally":
            selected_people = [person for person, var in zip(self.person_list.get_people(), self.checkbox_vars) if
                               var.get()]
        elif selected_option == "Unequally":
            amounts = [entry_var.get() for entry_var in self.amount_entries if hasattr(entry_var, 'get')]
            selected_people = list(zip(self.person_list.get_people(), amounts))

        description = self.description_entry.get()
        amount = self.amount_entry.get()
        paid_by = self.paid_by_var.get()

        # Get current date and time in the desired format
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        expense_info = {"description": description, "amount": amount, "paid_by": paid_by,
                        "split_method": selected_option, "date_time": date_time}

        # Append the expense information to the expenses list
        self.expenses_list.append(expense_info)

        # Add the expense to the Treeview
        self.expense_treeview.insert("", "end", values=(
            expense_info.get("description", ""),
            expense_info.get("amount", ""),
            expense_info.get("paid_by", ""),
            expense_info.get("split_method", ""),
            expense_info.get("date_time")  # Use "date_time" from expense_info
        ))
        # Clear the details in the Expense Details Tab
        self.reset_details()

    def add_expense_to_treeview(self):
        selected_option = self.split_var.get()

        if selected_option == "Equally":
            selected_people = [person for person, var in zip(self.person_list.get_people(), self.checkbox_vars) if
                               var.get()]
        elif selected_option == "Unequally":
            amounts = [entry_var.get() for entry_var in self.amount_entries if hasattr(entry_var, 'get')]
            selected_people = list(zip(self.person_list.get_people(), amounts))

        description = self.description_entry.get()
        amount = self.amount_entry.get()
        paid_by = self.paid_by_var.get()

        # Get current date and time in the desired format
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        expense_info = {"description": description, "amount": amount, "paid_by": paid_by,
                        "split_method": selected_option, "date_time": date_time}

        self.expenses_list.append(expense_info)
        self.expenses_text.insert(tk.END, self.get_expense_info_str(description, amount, paid_by, selected_option,
                                                                    date_time) + "\n")

        # Add the expense to the Treeview
        self.expense_treeview.insert("", "end", values=(
            expense_info.get("description", ""),
            expense_info.get("amount", ""),
            expense_info.get("paid_by", ""),
            expense_info.get("date_time", "")  # Use "date_time" from expense_info
        ))

    def display_expense_history(self):
        # Clear existing content in the Text widget
        self.expense_history_text.delete(1.0, tk.END)

        # Display expense history
        for expense_info in self.expenses_list:
            description = expense_info.get('description', '')
            amount = expense_info.get('amount', '')
            paid_by = expense_info.get('paid_by', '')
            split_method = expense_info.get('split_method', '')
            split_details = expense_info.get('split_details', '')

            expense_info_str = self.get_expense_info_str(description, amount, paid_by, split_method, split_details)
            self.expense_history_text.insert(tk.END, expense_info_str + "\n")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Expense Tracker")
    root.geometry("1003x564")

    image_0 = Image.open('C:\\Users\\User\\Pictures\\Blue Cream Aesthetic Illustration Group Project Presentation.jpg')
    bck_end = ImageTk.PhotoImage(image_0)
    lbl = tk.Label(root, image=bck_end)
    lbl.place(x=0, y=0)

    ttk.Label(root, text="WELCOME TO EQUIDEBT", style="Custom.TLabel", font=("Comic Sans MS", 20)).grid(row=0, column=1,
                                                                                                        padx=10,
                                                                                                        pady=10,
                                                                                                        sticky="w")
    style = ttk.Style()
    style.configure("Custom.TFrame", background="#5D869D")
    style.configure("Custom.TLabel", background="#5D869D", font=("Comic Sans MS", 10), foreground="#FFFFFF")
    style.configure("TButton", background="#20B2AA", font=("Comic Sans MS", 10), padding=5)

    authentication = Authentication()

    person_list_tab = ttk.Frame(root, style="Custom.TFrame")
    expense_app_tab = ttk.Frame(root, style="Custom.TFrame")


    # Create the PersonList instance here
    def on_successful_login(user):
        login_register_window.login_register_frame.destroy()
        person_list = PersonList(person_list_tab)  # Use the same instance created earlier
        expense_app = ExpenseApp(root, person_list, user)


    login_register_window = LoginRegisterWindow(root, authentication, on_successful_login)

    person_list = PersonList(person_list_tab)

    root.mainloop()
