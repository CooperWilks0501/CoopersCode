import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

TICKETS_FILE = 'tickets.json'

# Load existing tickets
def load_tickets():
    if os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, 'r') as f:
            return json.load(f)
    return []

# Save tickets to file
def save_tickets(tickets):
    with open(TICKETS_FILE, 'w') as f:
        json.dump(tickets, f, indent=4)

# Main app class
class TicketingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ticketing System")
        self.root.minsize(900, 400)  # Set minimum size

        self.tickets = load_tickets()

        # Form inputs
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="Low")
        self.description_var = tk.StringVar()

        self.create_form()
        self.create_ticket_list()

    def create_form(self):
        padding_opts = {'padx': 10, 'pady': 5}

        tk.Label(self.root, text="Name", font=("Arial", 12)).grid(row=0, column=0, sticky='w', **padding_opts)
        tk.Entry(self.root, textvariable=self.name_var, width=40).grid(row=0, column=1, **padding_opts)

        tk.Label(self.root, text="Email", font=("Arial", 12)).grid(row=1, column=0, sticky='w', **padding_opts)
        tk.Entry(self.root, textvariable=self.email_var, width=40).grid(row=1, column=1, **padding_opts)

        tk.Label(self.root, text="Priority", font=("Arial", 12)).grid(row=2, column=0, sticky='w', **padding_opts)
        priorities = ["Low", "Medium", "High"]
        ttk.Combobox(self.root, textvariable=self.priority_var, values=priorities, width=38).grid(row=2, column=1, **padding_opts)

        tk.Label(self.root, text="Description", font=("Arial", 12)).grid(row=3, column=0, sticky='nw', **padding_opts)
        self.desc_entry = tk.Text(self.root, height=6, width=40, font=("Arial", 10))
        self.desc_entry.grid(row=3, column=1, **padding_opts)

        tk.Button(self.root, text="Submit Ticket", command=self.submit_ticket, width=20, bg='lightblue').grid(row=4, column=1, pady=10)

    def create_ticket_list(self):
        tk.Label(self.root, text="Submitted Tickets", font=("Arial", 12, "bold")).grid(row=0, column=2, sticky='w', padx=10, pady=5)

        self.ticket_listbox = tk.Listbox(self.root, width=60, height=20, font=("Courier", 10))
        self.ticket_listbox.grid(row=1, column=2, rowspan=5, padx=20, pady=5, sticky='n')

        self.refresh_ticket_list()

    def refresh_ticket_list(self):
        self.ticket_listbox.delete(0, tk.END)
        for idx, ticket in enumerate(self.tickets):
            display = f"{idx+1}. [{ticket['priority']}] {ticket['name']} - {ticket['issue'][:40]}..."
            self.ticket_listbox.insert(tk.END, display)

    def submit_ticket(self):
        name = self.name_var.get()
        email = self.email_var.get()
        priority = self.priority_var.get()
        description = self.desc_entry.get("1.0", tk.END).strip()

        if not name or not email or not description:
            messagebox.showerror("Error", "All fields are required.")
            return

        ticket = {
            "name": name,
            "email": email,
            "priority": priority,
            "issue": description,
            "status": "Open"
        }

        self.tickets.append(ticket)
        save_tickets(self.tickets)

        messagebox.showinfo("Success", "Ticket submitted!")
        self.refresh_ticket_list()

        # Clear form
        self.name_var.set("")
        self.email_var.set("")
        self.priority_var.set("Low")
        self.desc_entry.delete("1.0", tk.END)

# Start the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TicketingApp(root)
    root.mainloop()
