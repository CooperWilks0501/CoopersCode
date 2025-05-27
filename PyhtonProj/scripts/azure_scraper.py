# Azure Documentation Scraper
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
import json
from urllib.parse import urljoin
import os

class AzureScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_urls = [
            'https://learn.microsoft.com/en-us/azure/security/',
            'https://learn.microsoft.com/en-us/azure/security-center/',
            'https://learn.microsoft.com/en-us/azure/sentinel/'
        ]
        self.visited_urls = set()
        self.azure_services = []
        self.security_practices = []

        # Set save directory
        self.save_dir = r'C:\Users\CWilk\Desktop\PyhtonProj\data'
        os.makedirs(self.save_dir, exist_ok=True)

    def scrape(self, max_pages=20):
        """Main scraping function"""
        print("Starting Azure documentation scrape...")
        pages_scraped = 0
        urls_to_visit = self.base_urls.copy()

        while urls_to_visit and pages_scraped < max_pages:
            current_url = urls_to_visit.pop(0)
            if current_url in self.visited_urls:
                continue

            print(f"Scraping: {current_url}")
            self.visited_urls.add(current_url)

            try:
                response = requests.get(current_url, headers=self.headers)
                if response.status_code != 200:
                    print(f"Failed to fetch {current_url}: {response.status_code}")
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')
                self.extract_services(soup, current_url)
                self.extract_security_practices(soup, current_url)
                new_links = self.extract_links(soup, current_url)

                for link in new_links:
                    if link not in self.visited_urls and link not in urls_to_visit:
                        urls_to_visit.append(link)

                pages_scraped += 1
                time.sleep(random.uniform(1, 2))

            except Exception as e:
                print(f"Error scraping {current_url}: {e}")

        print(f"Scraping complete. Visited {pages_scraped} pages.")
        print(f"Found {len(self.azure_services)} Azure services and {len(self.security_practices)} security practices.")
        self.save_results()

    def extract_links(self, soup, base_url):
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if not href or href.startswith(('#', 'javascript:', 'mailto:')):
                continue
            full_url = urljoin(base_url, href)
            if 'microsoft.com/en-us/azure/' in full_url:
                links.append(full_url)
        return links

    def extract_services(self, soup, url):
        headings = soup.find_all(['h1', 'h2', 'h3'])
        for heading in headings:
            text = heading.get_text().strip()
            if len(text) < 5 or text.lower() in ['overview', 'introduction', 'get started']:
                continue
            if 'Azure' in text:
                description = ""
                next_elem = heading.find_next('p')
                if next_elem:
                    description = next_elem.get_text().strip()
                service = {
                    'name': text,
                    'description': description,
                    'url': url,
                    'category': self.determine_category(text, description)
                }
                if not any(s['name'] == text for s in self.azure_services):
                    self.azure_services.append(service)

    def extract_security_practices(self, soup, url):
        security_keywords = ['security', 'protect', 'vulnerability', 'attack', 'threat', 'risk']
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.get_text().strip()
            if len(text) < 30:
                continue
            if any(keyword in text.lower() for keyword in security_keywords):
                heading = ""
                prev_heading = p.find_previous(['h1', 'h2', 'h3', 'h4'])
                if prev_heading:
                    heading = prev_heading.get_text().strip()
                practice = {
                    'title': heading,
                    'description': text,
                    'url': url,
                    'category': self.categorize_security_practice(text)
                }
                self.security_practices.append(practice)

    def determine_category(self, name, description):
        categories = {
            'Compute': ['vm', 'virtual machine', 'kubernetes', 'container', 'function'],
            'Storage': ['storage', 'blob', 'file', 'disk'],
            'Database': ['database', 'sql', 'cosmos', 'cache'],
            'Networking': ['network', 'firewall', 'dns', 'traffic'],
            'Security': ['security', 'sentinel', 'defender', 'key vault'],
            'Analytics': ['analytics', 'synapse', 'databricks', 'stream']
        }
        text = (name + " " + description).lower()
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        return "Other"

    def categorize_security_practice(self, text):
        categories = {
            'Authentication': ['authentication', 'identity', 'login', 'password', 'mfa'],
            'Data Protection': ['encryption', 'data protection', 'sensitive data'],
            'Network Security': ['network', 'firewall', 'nsg', 'ddos'],
            'Monitoring': ['monitor', 'alert', 'log', 'audit'],
            'Compliance': ['compliance', 'regulatory', 'standard', 'policy']
        }
        text = text.lower()
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        return "General Security"

    def save_results(self):
        # Save Azure services
        pd.DataFrame(self.azure_services).to_csv(os.path.join(self.save_dir, 'azure_services.csv'), index=False)
        
        # Save security practices
        pd.DataFrame(self.security_practices).to_csv(os.path.join(self.save_dir, 'security_practices.csv'), index=False)
        
        # Save as JSON too
        with open(os.path.join(self.save_dir, 'azure_data.json'), 'w') as f:
            json.dump({
                'services': self.azure_services,
                'security_practices': self.security_practices
            }, f, indent=2)

        print(f"Results saved to {self.save_dir}")

# Example usage
if __name__ == "__main__":
    scraper = AzureScraper()
    scraper.scrape(max_pages=20)
