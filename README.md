# Pre-orderManagementTool
A simple tool for pre-order management software. Fully offline
Installation instructions:
Make sure you have Python 3.x installed on your computer.
Install the required modules: tkinter, csv, datetime, tkcalendar, re, babel.
To install a module, you can use pip, the package installer for Python. For example, to install tkinter, you can use the command "pip install tkinter" in the command prompt or terminal.
Download the program files and save them in a directory on your computer.
Open the command prompt or terminal and navigate to the directory where the program files are saved.
Run the program by typing "python program_name.py" in the command prompt or terminal.

The MainApp class is a part of an Order Management System program. This class creates the main GUI window and provides buttons to call other classes that perform specific functions of the system.

To use this program, the following libraries need to be installed: tkinter, csv, datetime, tkcalendar, re, ttk, babel.

To use the MainApp class, simply create an instance of the class and pass in a tkinter master window. The program title will be set to "Order Management System". The class provides the following buttons:

"Place Preorders": calls the PlacePreorders class
"Update Orders": calls the UpdateOrders class
"Add Pre-order options": calls the ProductEntryUI class
"Remove Pre-order options": calls the DeletePreorderOptionsUI class
"Merge option files": calls the MergeCSV class
Clicking on any of these buttons will create a new tkinter Toplevel window and call the appropriate class to perform the desired function.

------------

The DeletePreorderOptionsUI class displays a list of pre-order options from a CSV file and allows the user to select and delete one or more options.

To use this class, import the necessary modules, including tkinter and csv. Then, create an instance of the DeletePreorderOptionsUI class, passing in a tkinter master window. The list of pre-order options will be displayed in a scrollable listbox. To delete one or more options, select them in the listbox and click the "Delete" button. A confirmation prompt will be displayed before the options are permanently deleted from the CSV file.

The class has two methods: load_options() and delete_selected(). The load_options() method reads the pre_order_options.csv file and adds each pre-order option to the listbox. The delete_selected() method gets the indices of the selected options from the listbox, prompts the user to confirm the deletion, and then deletes the selected options from the listbox and from the file.

Note: The CSV file must have a header row with the columns "Name", "Price", "UPC", "Release Date", and "Preorder Dates".

----

UpdateOrders class displays a list of orders loaded from a CSV file and allows the user to update the status of each order. The GUI for the class includes a table with headers, where each row displays the data for a single order, as well as a status selection widget and an update button for each row.

The __init__ method of the class initializes the GUI by creating a canvas widget and a set of headers for the table. It then loads the orders from the CSV file, skipping any that have already been picked up or canceled, and displays them in the table using either a Label or Entry widget for each field, depending on whether the field is read-only or not. For the status field, a Combobox widget is used to allow the user to select from a list of status options.

The update_order method is called when the user clicks the update button for a particular order. It updates the status and last contacted fields for the corresponding row in the CSV file and writes the updated data back to the file.

Overall, this code provides a simple but effective interface for viewing and updating a list of orders in a CSV file.


---------

The ProductEntryUI defines a UI for entering product information and submitting it to a CSV file. It contains input fields for product name, price, UPC, release date, and preorder dates. The "Submit" button writes the entered data to a CSV file and clears the input fields. After submission, a message box is displayed to confirm success.

The class uses the Tkinter library to create the UI and the csv library to write to the CSV file. The UI is created in the init method, which sets the title, size, and layout of the window, and creates the input fields and "Submit" button. The submit_form method is called when the "Submit" button is pressed, and it retrieves the entered data, writes it to the CSV file, clears the input fields, and displays a message box.


-------

The PlacePreorders class creates a form for customers to pre-order items. The form includes fields for the customer's first name, last name, email, phone number, expected delivery date, and a description of the item they want to pre-order.

The form loads pre-order options from a CSV file and creates a dropdown menu (combobox) of options for the customer to choose from. The dropdown menu can be filtered as the customer types in the description field.

The filter_options function filters the options in the dropdown menu based on the user's input. The submit function validates the input fields and, if they are valid, adds the customer's data to a CSV file.

After the customer submits the form, the input fields are cleared and a success message is displayed. However, the code doesn't include the code to clear the input fields and display the success message.


----

The MergeCSV class allows users to merge two CSV files. The GUI of the application is created using tkinter. The class has three methods:

init: Initializes the class and sets up the GUI. It creates a label for file1 and a button to select file2. It also creates a merge button and a label to show the status of the operation.

select_file2: Allows the user to select file2 using the file dialog box. It sets the file2_path variable and enables the merge button if a file is selected.

merge_files: Merges file2 into file1 if file2 is selected. It skips the header row of both files and writes rows from file2 to file1 if column A does not already exist in file1. It also removes any empty lines from the merged file. The status label is updated with the status of the operation.
