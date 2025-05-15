import requests
from bs4 import BeautifulSoup
import tkinter as tk

def fetch_temperatures():
    url = "https://weather.com/weather/tenday/l/4b5d5de52739fe4da6d11d7494c010994cfc9fad0e1125f5ff633d508403eacc"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Get the high and low temperature elements
    htemp = soup.find('span', class_='DailyContent--temp--axgOn')
    ltemp = soup.find('span', class_='DailyContent--temp--axgOn DailyContent--tempN--DPsDJ')

    high = htemp.text if htemp else "N/A"
    low = ltemp.text if ltemp else "N/A"

    return high, low


    # Get the percipitation 
def fetch_percipitation():
    url = "https://weather.com/weather/tenday/l/4b5d5de52739fe4da6d11d7494c010994cfc9fad0e1125f5ff633d508403eacc"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Get the percipitation element
    perc = soup.find('span', class_='DailyContent--value--Xgh8M')

    perc1 = perc.text
    return perc1


# Create a basic GUI window
root = tk.Tk()
root.title("Weather Forecast")
root.geometry("300x130")

# Fetch temperatures and precipitation
high_temp, low_temp = fetch_temperatures()
perc1 = fetch_percipitation()

label0 = tk.Label(root, text="Weather For Today")
label0.pack(anchor='center')

# Labels with arrows
label1 = tk.Label(root, text=f"▲ High: {high_temp}", font=("Arial", 14), fg="red")
label1.pack(pady=5)

label2 = tk.Label(root, text=f"▼ Low: {low_temp}", font=("Arial", 14), fg="blue")
label2.pack(pady=5)

label3 = tk.Label(root, text=f"🌧️ Precipitation: {perc1}", font=("Arial", 14), fg="green")
label3.pack(pady=5)

# Run the GUI
root.mainloop()
