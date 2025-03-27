# Eurorad Scraper

Eurorad Scraper is a Python package is build  to scrape case data from Eurorad and return it in json format.

## Installation

```sh
pip install euroradscraper
```

## Usage

### Importing the Package
```python
from euroradscraper.euroscraper import EuroradScraper
```

### Fetching a Case
```python
case_number = "189"  # Replace with an actual case number
scraper = EuroradScraper(case_number)
data = scraper.get_case_data()
print(data)
```

### Example Output
```json
{
    "case_number": "189",
    "title": "chest pain ",
    "details": {
        "Clinical History": "Patient with chest pain...",
        "Findings": "CT scan reveals..."
    },
    "images": [
        "https://www.eurorad.org/images/000443.png",
        "https://www.eurorad.org/images/143253.jpg"
    ]
}
```

## Features
- Fetches Eurorad case data using a case number.
- Extracts the case title, details, and images.
- Returns data in json format.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author

Your Name - [GitHub](https://github.com/santhosh1705kumar)