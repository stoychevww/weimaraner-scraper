# Weimaraner History Scraper

A Python web scraper specifically designed to extract historical information about Weimaraner dogs from the Czech Weimaraner Club website.

## Description

This script scrapes content from the [Czech Weimaraner Club history page](https://weimaraner-club.cz/chov/historie-vymarskych-oharu/) and converts it into structured JSON format. It extracts the main text content, organizes it into logical sections (theories about the breed's origin), and captures all images with their metadata.

## Features

- Extracts and organizes textual content into logical sections
- Captures all images with metadata (URL, dimensions, alt text, alignment)
- Handles Czech characters properly with UTF-8 encoding
- Normalizes relative image URLs to absolute paths
- Outputs structured data in JSON format

## Requirements

- Python 3.6+
- Required packages:
  - requests
  - beautifulsoup4

## Installation

1. Clone this repository or download the script:

```bash
git clone https://github.com/yourusername/weimaraner-scraper.git
cd weimaraner-scraper
```

2. Install the required packages:

```bash
pip install requests beautifulsoup4
```

## Usage

Run the script using Python:

```bash
python weimaraner_scraper.py
```

The script will generate a file named `weimaraner_history.json` containing the structured data.

## Output Format

The output JSON file has the following structure:

```json
{
  "title": "HISTORIE VÝMARSKÝCH OHAŘŮ",
  "url": "https://weimaraner-club.cz/chov/historie-vymarskych-oharu/",
  "sections": [
    {
      "type": "introduction",
      "content": [
        {
          "type": "paragraph",
          "text": "Výmarský ohař patří mezi nejstarší plemeno kontinentálních ohařů..."
        }
      ]
    },
    {
      "type": "theory",
      "title": "1. Teorie",
      "number": 1,
      "content": [
        {
          "type": "paragraph",
          "text": "Předpokládá se, že výmarští ohaři pocházejí pouze z jednoho předka...",
          "images": [
            {
              "url": "https://www.weimaraner-club.cz/wp-content/uploads/2021/08/Princ-Rupert-1.jpg",
              "filename": "Princ-Rupert-1.jpg",
              "alt": "",
              "width": "264",
              "height": "480",
              "classes": ["wp-image-10049", "alignright", "size-full"],
              "alignment": "right"
            }
          ]
        }
      ]
    }
  ],
  "all_images": [
    {
      "url": "https://www.weimaraner-club.cz/wp-content/uploads/2021/08/Princ-Rupert-1.jpg",
      "filename": "Princ-Rupert-1.jpg",
      "alt": "",
      "width": "264",
      "height": "480",
      "classes": ["wp-image-10049", "alignright", "size-full"]
    }
  ],
  "metadata": {
    "language": "cs",
    "scraped_at": "2025-04-02T12:34:56.789012"
  }
}
```

## Customization

You can modify the script to:

- Change the output file path by editing the line with `open('weimaraner_history.json', 'w', encoding='utf-8')`
- Scrape a different URL by changing the `url` variable
- Adjust the content organization logic by modifying the section handling code

## Legal Notice

This scraper is provided for educational purposes only. Please respect the website's terms of service and robots.txt file when using this script. Use responsibly and ensure you have permission to scrape content from the target website.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [Requests](https://requests.readthedocs.io/) for HTTP requests
- [Czech Weimaraner Club](https://weimaraner-club.cz/) for the historical information about Weimaraner dogs
