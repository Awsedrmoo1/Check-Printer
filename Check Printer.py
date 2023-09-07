import os
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from PIL import Image
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from NumberTranslator import SpellNumber

class NumberBox(tk.Frame):
    def __init__(chknum, master=None, default_value=1):
        super().__init__(master)
        chknum.value = default_value



        # Create entry to type in value
        chknum.entry = tk.Entry(chknum, width=6)
        chknum.entry.insert(0, f"{chknum.value:06d}")
        chknum.entry.pack(side=tk.LEFT)

        # Create buttons to increment/decrement value
        chknum.inc_button = tk.Button(chknum, text="+", command=chknum.increment)
        chknum.dec_button = tk.Button(chknum, text="-", command=chknum.decrement)
        chknum.inc_button.pack(side=tk.RIGHT, padx=(0, 5))
        chknum.dec_button.pack(side=tk.LEFT, padx=(5, 0))

        # Bind the return key to update the value
        chknum.entry.bind("<Return>", chknum.update_from_entry)
        

    def increment(chknum):
        chknum.value += 1
        chknum.update_display()

    def decrement(chknum):
        if chknum.value > 1:
            chknum.value -= 1
            chknum.update_display()

    def update_display(chknum):
        chknum.entry.delete(0, tk.END)
        chknum.entry.insert(0, f"{chknum.value:06d}")

    def update_from_entry(chknum, event):
        try:
            new_value = int(chknum.entry.get())
            if new_value > 0:
                chknum.value = new_value
                chknum.update_display()
        except ValueError:
            pass
    def get_value(chknum):
        return chknum.value



# Function to update payees.txt file
def update_payees_file(payees):
    with open("payees.txt", "w") as file:
        for payee in payees:
            file.write(payee + "\n")

# Function to add a new payee
def add_payee():
    new_payee = payee_entry.get().strip()
    if new_payee and new_payee not in payees:
        payees.append(new_payee)
        payee_entry["values"] = payees
        update_payees_file(payees)
        messagebox.showinfo("Success", f"{new_payee} added to the payee list.")
    else:
        messagebox.showerror("Error", "Please enter a unique payee name.")

# Function to delete a payee
def delete_payee():
    selected_payee = payee_entry.get().strip()
    if selected_payee:
        payees.remove(selected_payee)
        payee_entry["values"] = payees
        payee_entry.set('')
        update_payees_file(payees)
        messagebox.showinfo("Success", f"{selected_payee} deleted from the payee list.")
    else:
        messagebox.showerror("Error", "Please select a payee to delete.")

# Function to submit the form
def submit(image=True):
    payee = payee_entry.get()
    chknum = box.get_value()
    amount = amount_entry.get()
    payee_name = payee.split("_")[0]

    # Validate input
    try:
        fl_amount = float(amount)
        if fl_amount < 0:
            raise ValueError("Input cannot be negative")
    except ValueError as e:
        error_label.config(text=e, fg='red')
        return
    
    if fl_amount.is_integer():
        f_amount = "{:.2f}".format(fl_amount)
    else:
        f_amount = str(round(fl_amount, 2))

    # Create a new PDF file with the 4" x 8.5" page size
    page_width, page_height = landscape((3.7875 * inch, 8.5 * inch))
    if image == True:
        pdf_file = canvas.Canvas(f"{payee}_check_{box.get_value():06d}.pdf", pagesize=(page_width, page_height))
    else:
        pdf_file = canvas.Canvas(os.path.join(os.environ['TEMP'], f"{payee}_check_{box.get_value():06d}.pdf"), pagesize=(page_width, page_height))
    # Path to the image file
    img_path = "check.jpg"

    if image == True:
        pdf_file = canvas.Canvas(f"{payee}_check_{chknum:06d}.pdf", pagesize=(page_width, page_height))
    else:
        pdf_file = canvas.Canvas(os.path.join(os.environ['TEMP'], f"{payee}_check_{chknum:06d}-blank.pdf"), pagesize=(page_width, page_height))

    # Load the image and get its dimensions
    img = Image.open(img_path)
    width, height = img.size

    # Resize the image to fit the width of the page
    aspect_ratio = height / width
    img_width = page_width
    img_height = img_width * aspect_ratio
    img = img.resize((int(img_width), int(img_height)))

    # Set the image as the background
    if image == True:
        pdf_file.drawImage(img_path, 0, 0, img_width, img_height, preserveAspectRatio=True)

    # Set the font and size for the PDF
    pdf_file.setFont("Helvetica", 15)

    # Write the payee and amount to the PDF
    pdf_file.drawString(2 * inch, 2.25 * inch, payee)

    pdf_file.drawString(6.6 * inch, 2.26 * inch, f_amount)

    pdf_file.drawString(1.5 * inch, 1.93 * inch, f"{SpellNumber(amount)}")

    # Add today's date to the PDF
    today = datetime.today().strftime("%d%m%Y")
    today = " ".join(today)
    pdf_file.drawString(6.68 * inch, 2.75 * inch, today)

    pdf_file.showPage()

    # Save the PDF file
    pdf_file.save()


# Function to open the PDF file
def open_pdf():
    payee = payee_entry.get()
    filename = f"{payee}_check_{box.get_value():06d}.pdf"
    if os.path.exists(filename):
        os.startfile(filename)
    else:
        messagebox.showerror("Error", f"{filename} does not exist.")

def print_file():
    payee = payee_entry.get()
    submit(False)
    filename = os.path.join(os.environ['TEMP'], f"{payee}_check_{box.get_value():06d}.pdf")
    if os.path.exists(filename):
        os.startfile(filename)
    else:
        messagebox.showerror("Error", f"{filename} does not exist.")

# Read payees from file
if os.path.exists("payees.txt"):
    with open("payees.txt", "r") as file:
        payees = [line.strip() for line in file.readlines()]
else:
    payees = []



# Create the GUI
root = tk.Tk()
root.title("Payment Form")
root.geometry("470x250")
root.resizable(False, False)


# Add a title label
title_label = tk.Label(root, text="Check Printer", font=("Helvetica", 18, "bold"))
title_label.grid(row=0, column=1, columnspan=4, pady=10, sticky='w')

box = NumberBox(root)
box.grid(row=0, column=3, columnspan=4, pady=10, sticky='w')

# Add a payee label and dropdown list
payee_label = tk.Label(root, text="Payee:", font=("Helvetica", 12))
payee_label.grid(row=1, column=0, pady=5)
payee_entry = ttk.Combobox(root, values=payees, font=("Helvetica", 12))
payee_entry.grid(row=1, column=1, pady=5)

# Add an "Add Payee" button
add_button = tk.Button(root, text="Add Payee", command=add_payee, font=("Helvetica", 10))
add_button.grid(row=1, column=2, padx=5, pady=5)

# Add a "Delete Payee" button
delete_button = tk.Button(root, text="Delete Payee", command=delete_payee, font=("Helvetica", 10))
delete_button.grid(row=1, column=3, padx=5, pady=5)

# Add an amount label and entry
amount_label = tk.Label(root, text="Amount:", font=("Helvetica", 12))
amount_label.grid(row=2, column=0, pady=5)
amount_entry = tk.Entry(root, font=("Helvetica", 12))
amount_entry.grid(row=2, column=1, pady=5)

# Add an error label
error_label = tk.Label(root, fg='red', font=("Helvetica", 10))
error_label.grid(row=3, column=0, columnspan=2, pady=5)

# Add a "Submit" button
submit_button = tk.Button(root, text="Submit", command=submit, font=("Helvetica", 12))
submit_button.grid(row=4, column=0,  columnspan=2, padx=5, pady=10)

print_button = tk.Button(root, text="Print", command=print_file,font=("Helvetica", 12))
print_button.grid(row=4, column=1, columnspan=2, padx=5, pady=10)

# Add an "Open PDF" button
open_button = tk.Button(root, text="Open Preview", command=open_pdf, font=("Helvetica", 12))
open_button.grid(row=4, column=2, columnspan=2, padx=5, pady=10)

# Start the GUI
root.mainloop()

