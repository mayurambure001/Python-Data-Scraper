# import requests
# import json
# from bs4 import BeautifulSoup

# from bs4 import BeautifulSoup

# def fetch_data(html, tag, unique_class=None, unique_id=None):
#     soup = BeautifulSoup(html, "html.parser")
    
#     search_params = {}
#     if unique_class:
#         search_params['class_'] = unique_class
#     if unique_id:
#         search_params['id'] = unique_id
    
#     elements_list = [
#         el.get_text(strip=True) 
#         for el in soup.find_all(tag, **search_params)
#     ]
    
#     return elements_list

# def fetch_html(url, hdrs):
    
#     if isinstance(hdrs, str):
#         try:
#             hdrs = json.loads(hdrs)  # Works if JSON string
#         except json.JSONDecodeError:
#             raise ValueError("Headers string must be valid JSON with quotes around keys and values.")
#     try:
#         response = requests.get(url, headers=hdrs, timeout=10)
#         response.raise_for_status() 
#         return response.text
    
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching {url}: {e}")
#         return None


import re
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

def dynamic_scrape(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    text_content = soup.get_text(" ", strip=True)

    phone = re.search(r"\+?\d[\d\s\-\(\)]{7,}\d", text_content)
    phone = phone.group(0) if phone else None

    email = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text_content)
    email = email.group(0) if email else None

    name_tag = soup.find(["h1", "h2", "title"])
    name = name_tag.get_text(strip=True) if name_tag else None

    address = None
    for tag in soup.find_all(string=re.compile("address", re.I)):
        address = tag.parent.get_text(" ", strip=True)
        break

    return {
        "url": url,
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    }

if __name__ == "__main__":
    urls = ["https://www.mydrivingschoolpune.com"]
    results = [dynamic_scrape(u) for u in urls]
    print(results)

