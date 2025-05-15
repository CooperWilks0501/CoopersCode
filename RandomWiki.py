import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tkinter as tk
import webbrowser
from PIL import Image, ImageTk
from io import BytesIO

def get_random_wiki_url():
    try:
        response = requests.get("https://en.wikipedia.org/wiki/Special:Random", allow_redirects=True)
        return response.url
    except Exception as e:
        print(f"Error fetching random wiki URL: {e}")
        return None

def fetch_image_urls(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        imgs = soup.find_all('img')
        urls = []
        for img in imgs:
            src = img.get('src')
            if src and not src.endswith(".svg"):
                full_url = urljoin(url, src)
                urls.append(full_url)
        return urls
    except Exception as e:
        print(f"Error fetching images from {url}: {e}")
        return []

def get_tk_image_from_url(url, maxsize=(300, 300)):
    try:
        img_response = requests.get(url)
        img_response.raise_for_status()
        img_data = img_response.content
        pil_img = Image.open(BytesIO(img_data))
        pil_img.thumbnail(maxsize)
        return ImageTk.PhotoImage(pil_img)
    except Exception as e:
        print(f"Failed to load image {url}: {e}")
        return None

def open_link(event, url):
    webbrowser.open_new(url)

def load_random_article():
    # Clear previous content
    for widget in content_frame.winfo_children():
        widget.destroy()

    wiki_url = get_random_wiki_url()
    if wiki_url:
        # Clickable link at top
        link_label = tk.Label(content_frame, text=wiki_url, fg="blue", cursor="hand2", font=("Arial", 12, "underline"))
        link_label.pack(pady=10)
        link_label.bind("<Button-1>", lambda e: open_link(e, wiki_url))

        image_urls = fetch_image_urls(wiki_url)
        print(f"Images from: {wiki_url}")
        print("Found image URLs:", image_urls[:5])

        for i, img_url in enumerate(image_urls[:3]):
            tk_img = get_tk_image_from_url(img_url)
            if tk_img:
                label = tk.Label(content_frame, image=tk_img)
                label.image = tk_img  # Prevent garbage collection
                label.pack(padx=10, pady=10)
    else:
        label = tk.Label(content_frame, text="Could not fetch Wikipedia page.", font=("Arial", 14))
        label.pack(padx=10, pady=20)

# GUI setup
root = tk.Tk()
root.title("Random Wikipedia Images")
root.geometry("800x650")

# Scrollable content frame (optional)
content_frame = tk.Frame(root)
content_frame.pack(fill="both", expand=True)

# Randomize button at the bottom
randomize_button = tk.Button(root, text="Randomize", font=("Arial", 12), command=load_random_article)
randomize_button.pack(pady=10)

# Load initial content
load_random_article()

root.mainloop()
