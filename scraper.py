import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import re
from datetime import datetime

def scrape_weimaraner_history():
    # URL of the page to scrape
    url = "https://weimaraner-club.cz/chov/historie-vymarskych-oharu/"
    
    # User agent to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Send a GET request to the URL
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'  # Ensure correct encoding for Czech characters
        
        if response.status_code != 200:
            return {"error": f"Failed to fetch page: Status code {response.status_code}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the main content area
    content_area = soup.select_one('.et_pb_text_1 .et_pb_text_inner')
    
    if not content_area:
        return {"error": "Could not find main content area"}
    
    # Find the title
    title = soup.select_one('.et_pb_text_0 .et_pb_text_inner h1')
    title_text = title.text.strip() if title else ""
    
    # Extract all content
    sections = []
    current_section = {
        "type": "introduction",
        "content": []
    }
    
    # Get all elements in the content area
    for elem in content_area.children:
        if not hasattr(elem, 'name') or elem.name is None:
            continue
            
        if elem.name == 'h3':
            # Save the previous section
            if current_section["content"]:
                sections.append(current_section)
            
            # Start a new theory section
            theory_title = elem.text.strip()
            theory_number_match = re.search(r'(\d+)\.\s*Teorie', theory_title)
            theory_number = int(theory_number_match.group(1)) if theory_number_match else None
            
            current_section = {
                "type": "theory",
                "title": theory_title,
                "number": theory_number,
                "content": []
            }
            
        elif elem.name == 'p':
            # Skip paragraphs with class meta (author info)
            if elem.get('class') and 'meta' in elem.get('class'):
                continue
                
            # Extract text content
            text_content = elem.text.strip()
            
            # Extract images within this paragraph
            images = []
            for img in elem.find_all('img'):
                img_data = parse_image(img, url)
                if img_data:
                    # Check for alignment classes
                    if 'alignright' in img.get('class', []):
                        img_data['alignment'] = 'right'
                    elif 'alignleft' in img.get('class', []):
                        img_data['alignment'] = 'left'
                    elif 'aligncenter' in img.get('class', []):
                        img_data['alignment'] = 'center'
                    
                    images.append(img_data)
            
            # Add paragraph to current section
            paragraph_data = {
                "type": "paragraph",
                "text": text_content
            }
            
            if images:
                paragraph_data["images"] = images
                
            current_section["content"].append(paragraph_data)
            
        elif elem.name == 'ul':
            list_items = []
            for li in elem.find_all('li'):
                list_items.append(li.text.strip())
            
            current_section["content"].append({
                "type": "list",
                "items": list_items
            })
    
    # Add the last section
    if current_section["content"]:
        sections.append(current_section)
    
    # Extract all images for a separate list
    all_images = []
    for img in content_area.find_all('img'):
        img_data = parse_image(img, url)
        if img_data:
            all_images.append(img_data)
    
    # Compile results
    results = {
        "title": title_text,
        "url": url,
        "sections": sections,
        "all_images": all_images,
        "metadata": {
            "language": "cs",
            "scraped_at": datetime.now().isoformat()
        }
    }
    
    return results

def parse_image(img, base_url):
    """Parse an image element into a dictionary"""
    img_src = img.get('src', '')
    if not img_src:
        return None
        
    # Make sure we have a full URL
    if not img_src.startswith(('http://', 'https://')):
        img_src = urljoin(base_url, img_src)
    
    # Get the filename from the URL
    filename = img_src.split('/')[-1]
    
    return {
        "url": img_src,
        "filename": filename,
        "alt": img.get('alt', ''),
        "width": img.get('width', ''),
        "height": img.get('height', ''),
        "classes": img.get('class', [])
    }

if __name__ == "__main__":
    data = scrape_weimaraner_history()
    
    # Save to JSON file with proper encoding for Czech characters
    with open('weimaraner_history.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("Scraping completed. Data saved to weimaraner_history.json")