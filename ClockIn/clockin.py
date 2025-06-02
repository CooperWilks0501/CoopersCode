import tkinter as tk
from tkinter import messagebox
import json
import os
import sys
from datetime import datetime, timedelta
import pandas as pd
import subprocess

def get_app_folder():
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        return os.path.dirname(sys.executable)
    else:
        # Running as normal script
        return os.path.abspath(".")

DATA_FILE = os.path.join(get_app_folder(), "work_hours.json")
EXCEL_FILE = os.path.join(get_app_folder(), "weekly_report.xlsx")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

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

    log_text.config(state="disabled")  

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
    weekly_hours = calculate_weekly_hours()
    weekly_hours_label.config(text=weekly_hours)

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

def calculate_weekly_hours():
    data = load_data()
    today = datetime.today()
    # Find Monday of this week
    start_of_week = today - timedelta(days=today.weekday())
    total_seconds = 0

    for i in range(5):  # Monday to Friday
        day = start_of_week + timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        entry = data.get(day_str, {})
        clock_in = entry.get("clock_in")
        clock_out = entry.get("clock_out")

        if clock_in and clock_out:
            # parse time strings
            dt_in = datetime.strptime(f"{day_str} {clock_in}", "%Y-%m-%d %H:%M:%S")
            dt_out = datetime.strptime(f"{day_str} {clock_out}", "%Y-%m-%d %H:%M:%S")
            delta = dt_out - dt_in
            if delta.total_seconds() > 0:
                total_seconds += delta.total_seconds()

    hours = total_seconds / 3600
    return f"Weekly Hours (Mon-Fri): {hours:.2f}"

def export_to_excel():
    data = load_data()
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday

    week_start_str = start_of_week.strftime("%Y-%m-%d")

    rows = []
    for i in range(5):
        day = start_of_week + timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        entry = data.get(day_str, {})
        clock_in = entry.get("clock_in")
        clock_out = entry.get("clock_out")
        if clock_in and clock_out:
            dt_in = datetime.strptime(f"{day_str} {clock_in}", "%Y-%m-%d %H:%M:%S")
            dt_out = datetime.strptime(f"{day_str} {clock_out}", "%Y-%m-%d %H:%M:%S")
            delta = dt_out - dt_in
            hours = delta.total_seconds() / 3600 if delta.total_seconds() > 0 else 0
        else:
            hours = 0
        rows.append({"Date": day_str, "Clock In": clock_in or "", "Clock Out": clock_out or "", "Hours": round(hours, 2)})

    week_total = sum(r["Hours"] for r in rows)
    new_week_row = {"Week Start": week_start_str, "Total Hours": round(week_total, 2)}

    # Load or create DataFrame
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        # If week exists, overwrite it
        if week_start_str in df['Week Start'].astype(str).values:
            df.loc[df['Week Start'].astype(str) == week_start_str, 'Total Hours'] = round(week_total, 2)
        else:
            df = pd.concat([df, pd.DataFrame([new_week_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_week_row])

    df.to_excel(EXCEL_FILE, index=False)
    messagebox.showinfo("Exported", f"Weekly report exported to {EXCEL_FILE}")

def open_excel():
    if os.path.exists(EXCEL_FILE):
        try:
            os.startfile(EXCEL_FILE)  # Windows only
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Excel file: {e}")
    else:
        messagebox.showinfo("No File", "Excel file not found. Please export first.")

# GUI Setup
root = tk.Tk()
root.title("Work Hours Tracker")

clock_in_button = tk.Button(root, text="Clock In", command=clock_in, width=20, height=2)
clock_in_button.pack(pady=10)

clock_out_button = tk.Button(root, text="Clock Out", command=clock_out, width=20, height=2)
clock_out_button.pack(pady=10)

status_label = tk.Label(root, text="", font=("Arial", 12))
status_label.pack(pady=5)

weekly_hours_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
weekly_hours_label.pack(pady=5)

view_logs_button = tk.Button(root, text="View Work Logs", command=show_logs, width=20, height=2)
view_logs_button.pack(pady=10)

delete_button = tk.Button(root, text="Delete Today's Log", command=delete_today_log, width=20, height=2)
delete_button.pack(pady=10)

export_button = tk.Button(root, text="Export Weekly Report", command=export_to_excel, width=20, height=2)
export_button.pack(pady=10)

open_excel_button = tk.Button(root, text="Open Excel File", command=open_excel, width=20, height=2)
open_excel_button.pack(pady=10)

update_status()

root.mainloop()
