# scripts/main.py

from generate_data import generate_all_data
from azure_scraper import AzureScraper
from generate_activities import generate_activities_html 
from generate_FrontEnd import generate_frontend_html
from generate_users import generate_users_html
from generate_services import generate_services_html
from generate_resources import generate_resources_html
from generate_css import generate_css



if __name__ == "__main__":
    print("🔧 Running synthetic data generator...")
    generate_all_data()

    print("🌐 Running Azure documentation scraper...")
    scraper = AzureScraper()
    scraper.scrape(max_pages=20)

    print("Generating frontend HTML page...")
    generate_frontend_html()

    print("📝 Generating activities HTML page...")
    generate_activities_html()

    print('Generating users HTML page...')
    generate_users_html()

    print('Generating services HTML page...')
    generate_services_html()

    print('Generating services HTML page...')
    generate_resources_html()

    print('Generating CSS file...')
    generate_css()

    print("✅ All tasks complete! Data and HTML dashboard ready.")
