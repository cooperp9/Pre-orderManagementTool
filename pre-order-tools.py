import tkinter as tk
#from PlacePreorders import PlacePreorders
#from UpdateOrders import UpdateOrders
#from PreOrderOptionsUI import PreOrderOptionsUI
import csv
import datetime
from tkcalendar import DateEntry
from datetime import date
import re
from tkinter import ttk
from babel import numbers
from tkinter import filedialog

class MainApp:
    def __init__(self, master):
        self.master = master
        master.title("Order Management System")

        # Create buttons to call other classes
        self.place_orders_button = tk.Button(master, text="Place Preorders", command=self.place_preorders)
        self.place_orders_button.grid(row=0, column=0, padx=5, pady=5)

        self.update_orders_button = tk.Button(master, text="Update Orders", command=self.update_orders)
        self.update_orders_button.grid(row=0, column=1, padx=5, pady=5)

        self.ProductEntry_Button = tk.Button(master, text="Add Pre-order options", command=self.Update_PreOrderOptions)
        self.ProductEntry_Button.grid(row=0, column=2, padx=5, pady=5)
        
        self.RemoveProduct_Button = tk.Button(master, text="Remove Pre-order options", command=self.Remove_PreOrderOptions)
        self.RemoveProduct_Button.grid(row=1, column=1, padx=5, pady=5)
        
        self.Merge_csv_button = tk.Button(master, text = "Merge option files", command = self.Merge_CSV)
        self.Merge_csv_button.grid(row=1,column=0,padx=5,pady=5)

    def place_preorders(self):
        # Call PlacePreorders class
        self.new_window = tk.Toplevel(self.master)
        self.app = PlacePreorders(self.new_window)
        

    def update_orders(self):
        # Call UpdateOrders class
        self.new_window = tk.Toplevel(self.master)
        self.app = UpdateOrders(self.new_window)

    def Update_PreOrderOptions(self):
        # Call PreOrder class
        self.new_window = tk.Toplevel(self.master)
        self.app = ProductEntryUI(self.new_window)
        
    def Remove_PreOrderOptions(self):
        # Call PreOrder class
        self.new_window = tk.Toplevel(self.master)
        self.app = DeletePreorderOptionsUI(self.new_window)
        
    def Merge_CSV(self):
        #Call MergeCSV class
        self.new_window=tk.Toplevel(self.master)
        self.app=MergeCSV(self.new_window)
        
class DeletePreorderOptionsUI:
    def __init__(self, master):
        self.master = master
        master.title("Delete Preorder Options")

        # Create a frame for the list of pre-order options
        self.options_frame = tk.Frame(master)
        self.options_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Create a scrollable listbox to display the pre-order options
        self.options_listbox = tk.Listbox(self.options_frame, width=50, height=20)
        self.options_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Add a scrollbar to the listbox
        self.options_scrollbar = tk.Scrollbar(self.options_frame)
        self.options_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.options_listbox.config(yscrollcommand=self.options_scrollbar.set)
        self.options_scrollbar.config(command=self.options_listbox.yview)

        # Add a button to delete selected pre-order options
        self.delete_button = tk.Button(master, text="Delete", command=self.delete_selected)
        self.delete_button.pack(pady=10)

        # Load pre-order options from the file and display them in the listbox
        self.load_options()

    def load_options(self):
        # Open the pre_order_options.csv file and read its contents
        with open('pre_order_options.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader) # skip the header row
            for row in csv_reader:
                # Add each pre-order option to the listbox
                self.options_listbox.insert(tk.END, f"{row[0]} - ${row[1]} - {row[2]}")

    def delete_selected(self):
        # Get the indices of the selected pre-order options
        selected_indices = self.options_listbox.curselection()

        if not selected_indices:
            # If no options are selected, display an error message
            tk.messagebox.showerror("Error", "Please select one or more pre-order options to delete.")
        else:
            # Prompt the user to confirm the deletion
            confirm = tk.messagebox.askyesno("Confirm", "Are you sure you want to delete the selected pre-order option(s)?")

            if confirm:
                # Delete the selected options from the listbox and from the file
                with open('pre_order_options.csv', 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    rows = [row for row in csv_reader]
                with open('pre_order_options.csv', 'w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(['Name', 'Price', 'UPC', 'Release Date', 'Preorder Dates'])
                    for index, row in enumerate(rows):
                        if index not in selected_indices:
                            csv_writer.writerow(row)
                csv_file.close()  # Close the file
                self.options_listbox.delete(0, tk.END)
                self.load_options()

class UpdateOrders:
    def __init__(self, master):
        self.master = master
        master.title("View Orders")

        # Create canvas widget
        self.canvas = tk.Canvas(master)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create headers
        headers = ["First Name", "Last Name", "Email", "Phone", "Expected Delivery", "Description", "Status", "Last Contacted", "Actions"]
        header_width = 100
        for i, header in enumerate(headers):
            label = tk.Label(self.canvas, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5)
            self.canvas.columnconfigure(i, weight=1, minsize=header_width)

        # Load orders from CSV file and display
        with open("customer_data.csv", "r") as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if row[6] in ("Picked up", "Canceled"):
                    continue

                # Display order data in Entry or Label widgets
                for j, value in enumerate(row):
                    if j in (0, 1, 2, 3, 4, 5, 7):  # make non-status fields read-only
                        label = tk.Label(self.canvas, text=value, font=("Arial", 12))
                        label.grid(row=i+1, column=j, padx=5, pady=5, sticky="nsew")
                    else:
                        entry = tk.Entry(self.canvas, font=("Arial", 12))
                        entry.insert(0, value)
                        entry.grid(row=i+1, column=j, padx=5, pady=5, sticky="nsew")
                    self.canvas.columnconfigure(j, weight=1, minsize=header_width)

                # Create status selection widget
                status_var = tk.StringVar(value=row[6])
                status_widget = ttk.Combobox(self.canvas, textvariable=status_var, values=("In Transit", "Ready for pickup","Picked up","Canceled"))
                status_widget.grid(row=i+1, column=6, padx=5, pady=5, sticky="nsew")


                # Create update button
                update_button = tk.Button(self.canvas, text="Update", command=lambda i=i, status_var=status_var: self.update_order(i, status_var))
                update_button.grid(row=i+1, column=8, padx=5, pady=5, sticky="nsew")

    def update_order(self, i, status_var):
        # Update status and last contacted fields in CSV file
        with open("customer_data.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            rows[i][6] = status_var.get()
            rows[i][7] = date.today().strftime('%Y-%m-%d')

        with open("customer_data.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)


class ProductEntryUI:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Product Entry UI")
        self.parent.geometry("500x300")
        self.parent.resizable(False, False)
        
        # Create label and entry widgets for each input field
        tk.Label(self.parent, text="Product Name:").grid(row=0, column=0, padx=10, pady=10)
        self.product_name_entry = tk.Entry(self.parent)
        self.product_name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(self.parent, text="Price:").grid(row=1, column=0, padx=10, pady=10)
        self.price_entry = tk.Entry(self.parent)
        self.price_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.parent, text="MSRP:").grid(row=2, column=0, padx=10, pady=10)
        self.msrp_Entry = tk.Entry(self.parent)
        self.msrp_Entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(self.parent, text="UPC:").grid(row=3, column=0, padx=10, pady=10)
        self.upc_entry = tk.Entry(self.parent)
        self.upc_entry.grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(self.parent, text="Release Date:").grid(row=4, column=0, padx=10, pady=10)
        self.release_date_entry = DateEntry(self.parent, date_pattern='yyyy-mm-dd')
        self.release_date_entry.grid(row=4, column=1, padx=10, pady=10)
        
        tk.Label(self.parent, text="Preorder Dates:").grid(row=5, column=0, padx=10, pady=10)
        self.preorder_dates_entry = DateEntry(self.parent, date_pattern='yyyy-mm-dd')
        self.preorder_dates_entry.grid(row=5, column=1, padx=10, pady=10)

        
        
        # Create the "Submit" button
        self.submit_button = ttk.Button(self.parent, text="Submit", command=self.submit_form)
        self.submit_button.grid(row=6, column=1, padx=10, pady=10)
        
    def submit_form(self):
        # Get values from each input field
        product_name = self.product_name_entry.get()
        price = self.price_entry.get()
        msrp = self.msrp_Entry.get()
        upc = self.upc_entry.get()
        release_date = self.release_date_entry.get()
        preorder_dates = self.preorder_dates_entry.get()
        
        # Open the CSV file for writing and append the new row
        with open('pre_order_options.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([product_name, price,msrp, upc, release_date, preorder_dates])
        
        # Clear the input fields
        self.product_name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.msrp_Entry.delete(0, tk.END)
        self.upc_entry.delete(0, tk.END)
        self.release_date_entry.delete(0, tk.END)
        self.preorder_dates_entry.delete(0, tk.END)
        
        # Show a message box to confirm successful submission
        tk.messagebox.showinfo("Success", "Product information submitted successfully!")


class PlacePreorders:
    def __init__(self, master):
        self.master = master
        master.title("Preorder Form")
        master.geometry("800x800")

        self.filter_var = tk.StringVar()
        self.filter_var.trace("w", self.refresh_table)

        # Create input fields
        self.first_name_label = tk.Label(master, text="First Name:")
        self.first_name_label.place(relx=0.1, rely=0.05, relwidth=0.5, anchor="w")
        self.first_name_entry = tk.Entry(master)
        self.first_name_entry.place(relx=0.4, rely=0.05, relwidth=0.5, anchor="w")

        self.last_name_label = tk.Label(master, text="Last Name:")
        self.last_name_label.place(relx=0.1, rely=0.1, relwidth=0.5, anchor="w")
        self.last_name_entry = tk.Entry(master)
        self.last_name_entry.place(relx=0.4, rely=0.1, relwidth=0.5, anchor="w")

        self.email_label = tk.Label(master, text="Email:")
        self.email_label.place(relx=0.1, rely=0.15, relwidth=0.5, anchor="w")
        self.email_entry = tk.Entry(master)
        self.email_entry.place(relx=0.4, rely=0.15, relwidth=0.5, anchor="w")

        self.phone_label = tk.Label(master, text="Phone Number:")
        self.phone_label.place(relx=0.1, rely=0.2, relwidth=0.5, anchor="w")
        self.phone_entry = tk.Entry(master)
        self.phone_entry.place(relx=0.4, rely=0.2, relwidth=0.5, anchor="w")

        self.expected_delivery_label = tk.Label(master, text="Expected Delivery Date (YYYY-MM-DD):")
        self.expected_delivery_label.place(relx=0.1, rely=0.25, relwidth=0.5, anchor="w")
        self.expected_delivery = DateEntry(master, date_pattern='yyyy-mm-dd')
        self.expected_delivery.place(relx=0.4, rely=0.25, relwidth=0.5, anchor="w")

        # Create the filter entry box
        filter_label = tk.Label(master, text="Filter:")
        filter_label.place(relx=0.1, rely=0.3, relwidth=0.5, anchor="w")
        self.filter_entry = tk.Entry(master, textvariable=self.filter_var)
        self.filter_entry.place(relx=0.4, rely=0.3, relwidth=0.5, anchor="w")

        # Create the asset table
        self.table = ttk.Treeview(master, columns=("name", "price","MSRP", "upc", "release_date", "preorder_dates"), show="headings")
        self.table.place(relx=0.1, rely=0.5, relwidth=0.8, anchor="w")
        for idx, heading in enumerate(["Name", "Price","MSRP", "UPC", "Release Date", "Preorder Dates"]):
            self.table.heading(f"{idx}", text=heading)
            self.table.column(f"{idx}", width=200 if idx == 0 else 75 if idx == 1 else 100 if idx == 2 else 200)

        # Create vertical scrollbar
        vsb = ttk.Scrollbar(master, orient="vertical", command=self.table.yview)
        vsb.place(relx=0.9, rely=0.5, relheight=0.35, anchor="center")
        # Configure Treeview to use vertical scrollbar
        self.table.configure(yscrollcommand=vsb.set)

        # Create horizontal scrollbar
        hsb = ttk.Scrollbar(master, orient="horizontal", command=self.table.xview)
        hsb.place(relx=0.5, rely=0.85, relwidth=0.8, anchor="center")
        # Configure Treeview to use horizontal scrollbar
        self.table.configure(xscrollcommand=hsb.set)

        self.table.bind("<<TreeviewSelect>>", self.on_select)

        self.asset_list = []
        with open("pre_order_options.csv", "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # skip the header row
            self.asset_list = list(csv_reader)

        # Create error label
        self.error_label = tk.Label(master, fg="red")
        self.error_label.place(relx=0.1, rely=0.8,relwidth=0.5,  anchor="w")

        # Create submit button
        self.submit_button = tk.Button(master, text="Submit", command=self.submit)
        self.submit_button.place(relx=0.5, rely=.9,relwidth=0.5,  anchor="center")

        self.refresh_table()

    def on_select(self, event):
        selected_item = self.table.item(self.table.selection())["values"]
        self.selected_item = selected_item[0]
        
    def refresh_table(self, *_):
        # Clear the table
        self.table.delete(*self.table.get_children())

        # Filter the asset list
        filter_str = self.filter_var.get().lower()
        filtered_list = [asset for asset in self.asset_list if filter_str in asset[0].lower()]

        # Add the filtered assets to the table
        for asset in filtered_list:
            self.table.insert("", tk.END, values=asset)

        # Schedule another refresh after 1 second
        self.after(1000, self.refresh_table)    
    

    def submit(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        expected_delivery = self.expected_delivery.get()
        description = self.selected_item

        if not (first_name and last_name and expected_delivery and description and phone):
            error_message = "Please fill in all fields."
            self.error_label.config(text=error_message)
            return


        if not re.match(r"^\(?(\d{3})\)?[- ]?(\d{3})[- ]?(\d{4})$", phone):
            error_message = "Please enter a valid phone number."
            self.error_label.config(text=error_message)
            return

        # Verify expected delivery field is valid date
        if not re.match(r"\d{4}-\d{2}-\d{2}", expected_delivery):
            error_message = "Please enter a valid date (YYYY-MM-DD)."
            self.error_label.config(text=error_message)
            return

        # Add new customer data to CSV file
        with open("customer_data.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([first_name, last_name, email, phone, expected_delivery, description, "ordered", date.today()])

        # Clear input fields and show success message
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0,tk.END)
        self.expected_delivery.delete(0, tk.END)
        
class MergeCSV:

    def __init__(self, master):
        self.master = master
        self.file1_path = "pre_order_options.csv"
        self.file2_path = None

        self.file1_label = tk.Label(self.master, text="File 1: pre_order_options.csv")
        self.file1_label.grid(row=0, column=0, padx=10, pady=10)
        self.file1_label.grid(row=0, column=0, padx=10, pady=10)

        self.select_file2_button = tk.Button(self.master, text="Select File 2", command=self.select_file2)
        self.select_file2_button.grid(row=1, column=0, padx=10, pady=10)

        self.merge_button = tk.Button(self.master, text="Merge Files", command=self.merge_files, state=tk.DISABLED)
        self.merge_button.grid(row=2, column=0, padx=10, pady=10)

        self.status_label = tk.Label(self.master, text="")
        self.status_label.grid(row=3, column=0, padx=10, pady=10)

    def select_file2(self):
        # Allow the user to select file 2
        self.file2_path = filedialog.askopenfilename(title="Select file 2", filetypes=[("CSV files", "*.csv")])
        if self.file2_path:
            self.merge_button.config(state=tk.NORMAL)
            self.status_label.config(text="File 2 selected: " + self.file2_path)
        else:
            self.status_label.config(text="Please select a file")

    def merge_files(self):
        # Merge file2 into file1
        if not self.file2_path:
            self.status_label.config(text="Please select a file")
            return

        with open(self.file2_path, "r") as file2:
            reader2 = csv.reader(file2)
            next(reader2)  # skip the header row

            with open(self.file1_path, "r+") as file1:
                reader1 = csv.reader(file1)
                writer1 = csv.writer(file1)
                next(reader1)  # skip the header row

                # Create a set of existing values in file1 column A
                existing_values = set()
                for row in reader1:
                    existing_values.add(row[0])

                # Write rows from file2 to file1 if column A does not already exist
                for row in reader2:
                    if row[0] not in existing_values:
                        writer1.writerow(row)

                # Move the file pointer to the beginning of the file
                file1.seek(0)

                # Remove any empty lines from the merged file
                lines = file1.readlines()
                file1.seek(0)
                file1.truncate()
                for line in lines:
                    if not line.strip():
                        continue
                    file1.write(line)

        self.status_label.config(text="Files merged successfully!")



    

if __name__ == '__main__':
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

