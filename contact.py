import tkinter as tk
from tkinter import messagebox, simpledialog
import json

CONTACTS_FILE = 'contacts.json'

def load_contacts():
    """Load contacts from a JSON file."""
    try:
        with open(CONTACTS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_contacts(contacts):
    """Save contacts to a JSON file."""
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file, indent=4)

class ContactManagerApp:
    def __init__(self, root):
        self.contacts = load_contacts()
        self.root = root
        self.root.title("Contact Management System")

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        
        self.create_widgets()
        self.update_contact_list()

    def create_widgets(self):
        # Frame for contact details
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Entry(frame, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Entry(frame, textvariable=self.phone_var).grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Entry(frame, textvariable=self.email_var).grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Address:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Entry(frame, textvariable=self.address_var).grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        tk.Button(frame, text="Add Contact", command=self.add_contact).grid(row=4, column=0, padx=5, pady=5)
        tk.Button(frame, text="Update Contact", command=self.update_contact).grid(row=4, column=1, padx=5, pady=5)
        tk.Button(frame, text="Delete Contact", command=self.delete_contact).grid(row=4, column=2, padx=5, pady=5)
        tk.Button(frame, text="Search Contact", command=self.search_contact).grid(row=4, column=3, padx=5, pady=5)
        tk.Button(frame, text="View Contacts", command=self.update_contact_list).grid(row=4, column=4, padx=5, pady=5)

        # Contact list box
        self.contact_listbox = tk.Listbox(self.root, width=50)
        self.contact_listbox.pack(padx=10, pady=10)
        self.contact_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

    def add_contact(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()

        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and Phone are required.")
            return

        if name in self.contacts:
            messagebox.showwarning("Contact Exists", "Contact with this name already exists.")
            return

        self.contacts[name] = {
            'phone': phone,
            'email': email,
            'address': address
        }
        save_contacts(self.contacts)
        messagebox.showinfo("Success", "Contact added.")
        self.update_contact_list()
        self.clear_fields()

    def update_contact(self):
        selected_contact = self.contact_listbox.get(tk.ACTIVE)
        if not selected_contact:
            messagebox.showwarning("Selection Error", "Please select a contact to update.")
            return

        name = selected_contact.split(" - ")[0]

        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()

        if name in self.contacts:
            if phone:
                self.contacts[name]['phone'] = phone
            if email:
                self.contacts[name]['email'] = email
            if address:
                self.contacts[name]['address'] = address
            save_contacts(self.contacts)
            messagebox.showinfo("Success", "Contact updated.")
            self.update_contact_list()
        else:
            messagebox.showwarning("Error", "Contact not found.")

    def delete_contact(self):
        selected_contact = self.contact_listbox.get(tk.ACTIVE)
        if not selected_contact:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")
            return

        name = selected_contact.split(" - ")[0]

        if name in self.contacts:
            del self.contacts[name]
            save_contacts(self.contacts)
            messagebox.showinfo("Success", "Contact deleted.")
            self.update_contact_list()
        else:
            messagebox.showwarning("Error", "Contact not found.")

    def search_contact(self):
        search_term = simpledialog.askstring("Search", "Enter contact name or phone number:")
        if search_term:
            search_term = search_term.strip().lower()
            found = False
            for name, details in self.contacts.items():
                if search_term in name.lower() or search_term in details['phone']:
                    self.contact_listbox.delete(0, tk.END)
                    self.contact_listbox.insert(tk.END, f"{name} - {details['phone']}")
                    found = True
            if not found:
                messagebox.showinfo("Search Result", "No contact found.")

    def update_contact_list(self):
        self.contact_listbox.delete(0, tk.END)
        for name, details in self.contacts.items():
            self.contact_listbox.insert(tk.END, f"{name} - {details['phone']}")

    def on_listbox_select(self, event):
        selected_contact = self.contact_listbox.get(tk.ACTIVE)
        if selected_contact:
            name = selected_contact.split(" - ")[0]
            contact = self.contacts.get(name, {})
            self.name_var.set(name)
            self.phone_var.set(contact.get('phone', ''))
            self.email_var.set(contact.get('email', ''))
            self.address_var.set(contact.get('address', ''))

    def clear_fields(self):
        """Clear all input fields."""
        self.name_var.set('')
        self.phone_var.set('')
        self.email_var.set('')
        self.address_var.set('')

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerApp(root)
    root.mainloop()
