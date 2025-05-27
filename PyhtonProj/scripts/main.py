# scripts/main.py

from generate_data import generate_all_data
from azure_scraper import AzureScraper

if __name__ == "__main__":
    print("🔧 Running synthetic data generator...")
    generate_all_data()

    print("🌐 Running Azure documentation scraper...")
    scraper = AzureScraper()
    scraper.scrape(max_pages=20)

    print("✅ All data generated and saved to /data folder")
