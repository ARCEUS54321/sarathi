import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
from twilio.rest import Client
import os

# Twilio setup (load credentials from environment variables)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Path to the contacts file
contacts_file_path = r'C:\Projects\contacts.xlsx'

# Function to ensure the phone number is in E.164 format
def format_phone_number(phone_number, country_code='+91'):  # Default to India country code
    phone_number = str(phone_number)  # Convert the phone number to a string
    if not phone_number.startswith('+'):
        phone_number = country_code + phone_number
    return phone_number

# Function to send SMS
def send_sms(to_number, body):
    try:
        message = client.messages.create(
            body=body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        print(f"Sent message to {to_number}: {message.sid}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send message: {e}")

# Function when "Not Responded" is clicked
def not_responded():
    if os.path.exists(contacts_file_path):
        try:
            df = pd.read_excel(contacts_file_path)
            if df.empty:
                messagebox.showwarning("Warning", "No contacts in the Excel file. Please insert contact details.")
            else:
                for index, row in df.iterrows():
                    phone_number = format_phone_number(row['Phone Number'])
                    print(f"Sending message to {phone_number}")
                    send_sms(phone_number, "EMERGENCY WARNING! ")
                messagebox.showinfo("Info", "Messages have been sent.")
        except Exception as e:
            messagebox.showerror("Error", f"Error reading contacts file: {e}")
    else:
        # Create a new contacts file
        try:
            df = pd.DataFrame(columns=["Contact Name", "Phone Number"])
            df.to_excel(contacts_file_path, index=False)
            messagebox.showwarning("Warning", "Contacts file was not found. A new file has been created. Please insert contact details.")
        except Exception as e:
            messagebox.showerror("Error", f"Error creating contacts file: {e}")

# Function when "Driver Responded" is clicked
def driver_responded():
    messagebox.showinfo("Info", "Driver has responded.")

# Function to add a new contact
def add_contact():
    new_contact_name = simpledialog.askstring("Input", "Enter the contact name:")
    new_contact_phone = simpledialog.askstring("Input", "Enter the phone number (with country code):")

    if new_contact_name and new_contact_phone:
        try:
            if os.path.exists(contacts_file_path):
                df = pd.read_excel(contacts_file_path)
            else:
                df = pd.DataFrame(columns=["Contact Name", "Phone Number"])

            new_contact = pd.DataFrame({"Contact Name": [new_contact_name], "Phone Number": [new_contact_phone]})
            df = pd.concat([df, new_contact], ignore_index=True)
            df.to_excel(contacts_file_path, index=False)
            messagebox.showinfo("Info", "New contact has been added.")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding contact: {e}")
    else:
        messagebox.showwarning("Warning", "Please enter valid details.")

# Create the main application window
root = tk.Tk()
root.title("Driver Response Application")

# Create buttons
btn_driver_responded = tk.Button(root, text="Driver Responded", command=driver_responded)
btn_not_responded = tk.Button(root, text="Not Responded", command=not_responded)
btn_add_contact = tk.Button(root, text="Add New Contact", command=add_contact)

# Place the buttons in the window
btn_driver_responded.pack(pady=10)
btn_not_responded.pack(pady=10)
btn_add_contact.pack(pady=10)

# Run the application
root.mainloop()
