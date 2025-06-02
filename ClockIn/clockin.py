import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

DATA_FILE = "work_hours.json"

def show_logs():
    data = load_data()

    log_window = tk.Toplevel(root)
    log_window.title("Work Log History")
    log_window.geometry("400x400")

    log_text = tk.Text(log_window, wrap="word")
    log_text.pack(expand=True, fill="both")

    if not data:
        log_text.insert("end", "No data logged yet.")
    else:
        for date in sorted(data.keys()):
            entry = data[date]
            clock_in = entry.get("clock_in", "Not recorded")
            clock_out = entry.get("clock_out", "Not recorded")
            log_text.insert("end", f"Date: {date}\n  Clocked In: {clock_in}\n  Clocked Out: {clock_out}\n\n")

    log_text.config(state="disabled")  # Make read-only

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def clock_in():
    today = datetime.today().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")

    data = load_data()

    if today in data and data[today].get("clock_in"):
        messagebox.showinfo("Already Clocked In", f"Already clocked in today at {data[today]['clock_in']}.")
        return

    data.setdefault(today, {})["clock_in"] = now
    save_data(data)
    update_status()
    messagebox.showinfo("Clock In", f"Clocked in at {now}.")

def clock_out():
    today = datetime.today().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")

    data = load_data()

    if today not in data or not data[today].get("clock_in"):
        messagebox.showwarning("Not Clocked In", "You must clock in before clocking out.")
        return

    data[today]["clock_out"] = now
    save_data(data)
    update_status()
    messagebox.showinfo("Clock Out", f"Clocked out at {now}.")

def update_status():
    data = load_data()
    today = datetime.today().strftime("%Y-%m-%d")
    if today in data:
        ci = data[today].get("clock_in", "Not clocked in")
        co = data[today].get("clock_out", "Not clocked out")
    else:
        ci, co = "Not clocked in", "Not clocked out"
    
    status_label.config(text=f"Today ({today})\nClock In: {ci}\nClock Out: {co}")



def delete_today_log():
    today = datetime.today().strftime("%Y-%m-%d")
    data = load_data()

    if today in data:
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete today's log ({today})?")
        if confirm:
            del data[today]
            save_data(data)
            update_status()
            messagebox.showinfo("Deleted", "Today's log has been deleted.")
    else:
        messagebox.showinfo("No Entry", "No log found for today.")

# --- GUI Setup ---
root = tk.Tk()
root.title("Work Hours Tracker")

clock_in_button = tk.Button(root, text="Clock In", command=clock_in, width=20, height=2)
clock_in_button.pack(pady=10)

clock_out_button = tk.Button(root, text="Clock Out", command=clock_out, width=20, height=2)
clock_out_button.pack(pady=10)

status_label = tk.Label(root, text="", font=("Arial", 12))
status_label.pack(pady=20)

view_logs_button = tk.Button(root, text="View Work Logs", command=show_logs, width=20, height=2)
view_logs_button.pack(pady=10)

delete_button = tk.Button(root, text="Delete Today's Log", command=delete_today_log, width=20, height=2)
delete_button.pack(pady=10)


update_status()

root.mainloop()
