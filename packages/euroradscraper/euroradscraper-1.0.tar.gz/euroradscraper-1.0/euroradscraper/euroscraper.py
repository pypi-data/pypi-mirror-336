import requests
from bs4 import BeautifulSoup
import json

class EuroradScraper:
    BASE_URL = "https://www.eurorad.org/case/"
    
    def __init__(self, case_number):
        self.case_number = case_number
        self.url = f"{self.BASE_URL}{case_number}"
    
    def fetch_case(self):
        response = requests.get(self.url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch case {self.case_number}")
        return response.text
    
    def parse_case(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extracting title
        title_tag = soup.find('h1')
        title = title_tag.text.strip() if title_tag else "Unknown"
        
        # Extracting case details
        details = {}
        detail_sections = soup.find_all('div', class_='case-section')
        for section in detail_sections:
            heading = section.find('h2')
            content = section.find('p')
            if heading and content:
                details[heading.text.strip()] = content.text.strip()
        
        # Extracting images
        images = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs]
        
        return {
            "case_number": self.case_number,
            "title": title,
            "details": details,
            "images": images
        }
    
    def get_case_data(self):
        html = self.fetch_case()
        return self.parse_case(html)
