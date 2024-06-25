import tkinter as tk
from tkinter import messagebox


class RestaurantManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Management System")
        self.customer_name = tk.StringVar()
        self.customer_contact = tk.StringVar()

        # Food Appetizer list
        self.food_appetizers = {
            "Nachos": 5,
            "French Fries": 5,
            "Buffalo chicken wings": 7,
            "Potato Skins": 7,
            "Crab Cakes": 6
        }

        # Main Courses list
        self.main_courses = {
            "Honey Garlic Chicken": 20,
            "Pan-Seared Salmon": 25,
            "Lemon Chicken Pasta": 24,
            "Steak Diane": 30,
            "Creamy Chicken Noodle Soup": 32
        }

        # Desserts list
        self.desserts = {
            "Cheesy Brownie": 10,
            "Chocolate Cake": 12,
            "Ice Cream": 5,
            "Italian Tiramisu": 11,
            "Cookies and Cream": 12
        }

        self.orders = {}
        self.gst_percentage = 18
        self.create_gui()

    # GUI creation for program
    def create_gui(self):
        details_frame = tk.LabelFrame(self.root, text="Customer Details")
        details_frame.pack(fill="x", padx=10, pady=10)

        name_label = tk.Label(details_frame, text="Customer Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(details_frame, textvariable=self.customer_name)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        contact_label = tk.Label(details_frame, text="Contact Number:")
        contact_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        contact_entry = tk.Entry(details_frame, textvariable=self.customer_contact, validate="key")
        contact_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        contact_entry.configure(validatecommand=(contact_entry.register(self.validate_contact), "%P"))

        menu_frame = tk.LabelFrame(self.root, text="Restaurant Menu")
        menu_frame.pack(fill="both", expand=True, padx=10, pady=10)

        row = 0
        for category, items in [("Appetizers", self.food_appetizers), ("Main Courses", self.main_courses),
                                ("Desserts", self.desserts)]:
            category_label = tk.Label(menu_frame, text=category)
            category_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
            quantity_header = tk.Label(menu_frame, text="Quantity")
            quantity_header.grid(row=row, column=1, padx=5, pady=5, sticky="w")
            row += 1

            for item, price in items.items():
                var = tk.IntVar()
                item_label = tk.Label(menu_frame, text=f"{item} - {self.convert_to_inr(price)}")
                item_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
                quantity_entry = tk.Entry(menu_frame, width=5)
                quantity_entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")

                self.orders[item] = {"var": var, "quantity": quantity_entry}
                row += 1

        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(fill="x", padx=10, pady=10)

        print_bill_button = tk.Button(buttons_frame, text="Print Bill", command=self.show_bill_popup)
        print_bill_button.pack(side="left", padx=5)

        past_record_button = tk.Button(buttons_frame, text="Past Records", command=self.past_records)
        past_record_button.pack(side="left", padx=5)

        clear_selection_button = tk.Button(buttons_frame, text="Clear Selection", command=self.clear_selection)
        clear_selection_button.pack(side="left", padx=5)

        self.sample_bill_text = tk.Text(self.root, height=10)
        self.sample_bill_text.pack(fill="x", padx=10, pady=10)

        for item, info in self.orders.items():
            info["quantity"].bind("<FocusOut>", lambda event, item=item: self.update_sample_bill(item))
            info["quantity"].bind("<Return>", lambda event, item=item: self.update_sample_bill(item))
            info["quantity"].bind("<KeyRelease>", lambda event, item=item: self.update_sample_bill(item))
            info["var"].trace("w", lambda *args, item=item: self.update_sample_bill(item))

    # Showing the bill to the user
    def show_bill_popup(self):
        if not self.customer_name.get().strip():
            messagebox.showwarning("Warning", "Please enter the customer name.")
            return

        selected_items = []
        total_price = 0
        for item, info in self.orders.items():
            quantity = info["quantity"].get()
            if quantity:
                selected_items.append((item, int(quantity)))
                if item in self.food_appetizers:
                    total_price += self.food_appetizers[item] * int(quantity)
                elif item in self.main_courses:
                    total_price += self.main_courses[item] * int(quantity)
                elif item in self.desserts:
                    total_price += self.desserts[item] * int(quantity)

        if not selected_items:
            messagebox.showwarning("Warning", "Please select at least one item.")
            return

        gst_amount = (total_price * self.gst_percentage) / 100
        bill = f"Customer Name: {self.customer_name.get()}\n"
        bill += f"Customer Contact: {self.customer_contact.get()}\n\n"
        bill += "Selected Items:\n"
        for item, quantity in selected_items:
            if item in self.food_appetizers:
                price = self.food_appetizers[item]
            elif item in self.main_courses:
                price = self.main_courses[item]
            elif item in self.desserts:
                price = self.desserts[item]
            bill += f"{item} x {quantity} - {self.convert_to_inr(price * quantity)}\n"
        bill += f"\nTotal Price: {self.convert_to_inr(total_price)}\n"
        bill += f"GST ({self.gst_percentage}%): {self.convert_to_inr(gst_amount)}\n"
        bill += f"Total Amount: {self.convert_to_inr(total_price + gst_amount)}"

        messagebox.showinfo("Bill", bill)

    # Showing past records of bill to user
    def past_records(self):
        messagebox.showinfo("Past Records", "This feature is not yet implemented.")

    # Option to clear past records of bill
    def clear_selection(self):
        for item, info in self.orders.items():
            info["var"].set(0)
            info["quantity"].delete(0, tk.END)

    # Live update of the bill according to user input
    def update_sample_bill(self, item):
        selected_items = []
        total_price = 0

        for item, info in self.orders.items():
            quantity = info["quantity"].get()
            if quantity:
                selected_items.append((item, int(quantity)))
                if item in self.food_appetizers:
                    total_price += self.food_appetizers[item] * int(quantity)
                elif item in self.main_courses:
                    total_price += self.main_courses[item] * int(quantity)
                elif item in self.desserts:
                    total_price += self.desserts[item] * int(quantity)

        gst_amount = (total_price * self.gst_percentage) / 100
        bill = f"Customer Name: {self.customer_name.get()}\n"
        bill += f"Customer Contact: {self.customer_contact.get()}\n\n"
        bill += "Selected Items:\n"
        for item, quantity in selected_items:
            if item in self.food_appetizers:
                price = self.food_appetizers[item]
            elif item in self.main_courses:
                price = self.main_courses[item]
            elif item in self.desserts:
                price = self.desserts[item]
            bill += f"{item} x {quantity} - {self.convert_to_inr(price * quantity)}\n"
        bill += f"\nTotal Price: {self.convert_to_inr(total_price)}\n"
        bill += f"GST ({self.gst_percentage}%): {self.convert_to_inr(gst_amount)}\n"
        bill += f"Total Amount: {self.convert_to_inr(total_price + gst_amount)}"

        self.sample_bill_text.delete(1.0, tk.END)
        self.sample_bill_text.insert(tk.END, bill)

    def validate_contact(self, new_value):
        return new_value.isdigit() or new_value == ""

    @staticmethod
    def convert_to_inr(amount):
        return "£" + str(amount)


root = tk.Tk()
app = RestaurantManagementSystem(root)
root.mainloop()
