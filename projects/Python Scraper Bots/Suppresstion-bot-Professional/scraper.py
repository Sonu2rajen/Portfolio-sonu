"""
Amazon.in Scraper Module
Scrapes Availability, Asin Search (YES/NO), and Asin Reflect for each ASIN
"""

import requests
import time
import random
import re
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }

def extract_asin_from_url(url):
    """Extract ASIN from the final URL after redirects"""
    patterns = [
        r'/dp/([A-Z0-9]{10})',
        r'/product/([A-Z0-9]{10})',
        r'asin=([A-Z0-9]{10})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def extract_asin_from_page(soup):
    """Extract ASIN from the product detail / additional info table on the page"""
    # Method 1: Look in product details table
    detail_sections = soup.find_all(['table', 'div'], class_=re.compile(r'detail|technical|product-facts|a-expander', re.I))
    for section in detail_sections:
        rows = section.find_all('tr')
        for row in rows:
            cells = row.find_all(['th', 'td'])
            for i, cell in enumerate(cells):
                if 'ASIN' in cell.get_text():
                    if i + 1 < len(cells):
                        asin_text = cells[i + 1].get_text().strip()
                        if re.match(r'^[A-Z0-9]{10}$', asin_text):
                            return asin_text

    # Method 2: Look for ASIN in list items
    for li in soup.find_all('li'):
        text = li.get_text()
        if 'ASIN' in text:
            match = re.search(r'ASIN[:\s]+([A-Z0-9]{10})', text)
            if match:
                return match.group(1)

    # Method 3: Look in span elements with specific patterns
    for span in soup.find_all('span'):
        text = span.get_text().strip()
        if re.match(r'^[A-Z0-9]{10}$', text):
            prev = span.find_previous('span')
            if prev and 'ASIN' in prev.get_text():
                return text

    # Method 4: Check data attributes and hidden inputs
    asin_input = soup.find('input', {'id': 'ASIN'})
    if asin_input:
        return asin_input.get('value', '').strip()

    # Method 5: Search entire page text
    page_text = soup.get_text()
    match = re.search(r'\bASIN[:\s]+([A-Z0-9]{10})\b', page_text)
    if match:
        return match.group(1)

    return None

def extract_availability(soup):
    """Extract availability text from the product page"""
    # Method 1: Standard availability div
    availability_div = soup.find('div', {'id': 'availability'})
    if availability_div:
        span = availability_div.find('span')
        if span:
            return span.get_text().strip()

    # Method 2: Look for add to cart button (means in stock)
    add_to_cart = soup.find('input', {'id': 'add-to-cart-button'})
    if add_to_cart:
        return "In stock"

    # Method 3: Buy now button
    buy_now = soup.find('input', {'id': 'buy-now-button'})
    if buy_now:
        return "In stock"

    # Method 4: Out of stock message
    page_text = soup.get_text().lower()
    if 'currently unavailable' in page_text:
        return "Currently unavailable."
    if 'out of stock' in page_text:
        return "Currently unavailable."
    if 'in stock' in page_text:
        return "In stock"

    return "Currently unavailable."

def scrape_asin(searched_asin, delay_min=2, delay_max=5, retries=3):
    """
    Scrape a single ASIN from Amazon.in
    Returns dict with: ASIN, Availability, Asin Search, Asin Reflect
    """
    url = f"https://www.amazon.in/dp/{searched_asin}?th=1"
    result = {
        "ASIN": searched_asin,
        "Availability": "Error occured",
        "Asin Search": "No",
        "Asin Refelct": "Error occured"
    }

    for attempt in range(retries):
        try:
            session = requests.Session()
            response = session.get(
                url,
                headers=get_headers(),
                timeout=20,
                allow_redirects=True
            )

            # Check final URL after redirects
            final_url = response.url
            url_asin = extract_asin_from_url(final_url)

            if response.status_code == 503 or 'robot' in response.text.lower()[:500]:
                logger.warning(f"ASIN {searched_asin}: Bot detected on attempt {attempt+1}, waiting...")
                time.sleep(random.uniform(10, 20))
                continue

            if response.status_code == 404:
                result["Availability"] = "Currently unavailable."
                result["Asin Search"] = "No"
                result["Asin Refelct"] = searched_asin
                return result

            if response.status_code != 200:
                logger.warning(f"ASIN {searched_asin}: Status {response.status_code} on attempt {attempt+1}")
                time.sleep(random.uniform(5, 10))
                continue

            soup = BeautifulSoup(response.content, 'lxml')

            # Extract availability
            availability = extract_availability(soup)

            # Extract ASIN from page (additional info section)
            page_asin = extract_asin_from_page(soup)

            # Determine Asin Reflect
            if page_asin:
                asin_reflect = page_asin
            elif url_asin:
                asin_reflect = url_asin
            else:
                asin_reflect = searched_asin

            # Determine Asin Search (YES if page shows searched ASIN's data)
            if page_asin and page_asin == searched_asin:
                asin_search = "Yes"
            elif not page_asin and url_asin and url_asin == searched_asin:
                asin_search = "Yes"
            elif url_asin and url_asin != searched_asin:
                asin_search = "No"
                logger.info(f"ASIN {searched_asin}: Redirected to {url_asin}")
            else:
                asin_search = "Yes"

            result = {
                "ASIN": searched_asin,
                "Availability": availability,
                "Asin Search": asin_search,
                "Asin Refelct": asin_reflect
            }

            logger.info(f"✓ {searched_asin} | {availability} | Search:{asin_search} | Reflect:{asin_reflect}")
            return result

        except requests.exceptions.Timeout:
            logger.warning(f"ASIN {searched_asin}: Timeout on attempt {attempt+1}")
            result = {
                "ASIN": searched_asin,
                "Availability": "Timeout Error",
                "Asin Search": "No",
                "Asin Refelct": "Timeout Error"
            }
            if attempt < retries - 1:
                time.sleep(random.uniform(5, 10))

        except requests.exceptions.ConnectionError as e:
            logger.warning(f"ASIN {searched_asin}: Connection error on attempt {attempt+1}: {e}")
            result = {
                "ASIN": searched_asin,
                "Availability": "Error occured",
                "Asin Search": "No",
                "Asin Refelct": "Error occured"
            }
            if attempt < retries - 1:
                time.sleep(random.uniform(5, 10))

        except Exception as e:
            logger.error(f"ASIN {searched_asin}: Unexpected error: {e}")
            result = {
                "ASIN": searched_asin,
                "Availability": "Error occured",
                "Asin Search": "No",
                "Asin Refelct": "Error occured"
            }

    return result

def scrape_all_asins(asin_list, delay_min=2, delay_max=5, retries=3, progress_callback=None):
    """
    Scrape all ASINs with delay between requests
    Returns list of result dicts
    """
    results = []
    total = len(asin_list)

    logger.info(f"Starting scrape of {total} ASINs...")

    for i, asin in enumerate(asin_list, 1):
        asin = str(asin).strip()
        if not asin or asin == 'nan':
            continue

        logger.info(f"[{i}/{total}] Scraping {asin}...")

        result = scrape_asin(asin, delay_min, delay_max, retries)
        results.append(result)

        if progress_callback:
            progress_callback(i, total, asin, result)

        # Delay between requests (slightly longer every 50 ASINs)
        if i % 50 == 0:
            logger.info(f"Processed {i}/{total} ASINs. Taking a longer break...")
            time.sleep(random.uniform(15, 25))
        else:
            time.sleep(random.uniform(delay_min, delay_max))

    logger.info(f"Scraping complete. {len(results)} results collected.")
    return results
