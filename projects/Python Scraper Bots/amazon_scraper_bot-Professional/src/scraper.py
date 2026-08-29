from playwright.sync_api import sync_playwright
from utils import random_delay
import re

AMAZON_URL = "https://www.amazon.in/dp/{}"

def scrape_asin(asin):
    result = {
        "Date": "",
        "ASIN": asin,
        "Ratings": "",
        "Total Ratings": "",
        "Availability": "",
        "Price": "",
        "Seller Name": "",
        "ASIN Search": "NO",
        "ASIN Reflect": "NO"
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        page.goto(AMAZON_URL.format(asin), timeout=60000)

        # 🔴 CRITICAL WAIT — BUY BOX
        try:
            page.wait_for_selector(
                "#add-to-cart-button, #buy-now-button",
                timeout=20000
            )
        except:
            browser.close()
            return result

        # Product title must exist
        if not page.locator("#productTitle").count():
            browser.close()
            return result

        # ---------- ASIN FROM ADDITIONAL INFORMATION ----------
        asin_found = ""
        try:
            rows = page.locator("#detailBullets_feature_div li").all()
            for row in rows:
                text = row.inner_text()
                if "ASIN" in text:
                    asin_found = text.split(":")[-1].strip()
                    break
        except:
            pass

        if asin_found == asin:
            result["ASIN Reflect"] = "YES"
            result["ASIN Search"] = "YES"
        else:
            browser.close()
            return result   # suppressed / replaced ASIN

        # ---------- RATINGS ----------
        try:
            rating_text = page.locator("span.a-icon-alt").first.inner_text()
            result["Ratings"] = rating_text.split()[0]
        except:
            pass

        # ---------- TOTAL RATINGS ----------
        try:
            review_text = page.locator("#acrCustomerReviewText").inner_text()
            result["Total Ratings"] = re.sub(r"[^\d]", "", review_text)
        except:
            pass

        # ---------- AVAILABILITY ----------
        try:
            availability = page.locator("#availability span").inner_text().lower()
            if "in stock" in availability:
                result["Availability"] = "Stock Available"
            else:
                result["Availability"] = "Out of Stock"
        except:
            result["Availability"] = "Out of Stock"

        # ---------- PRICE ----------
        try:
            result["Price"] = page.locator("span.a-price-whole").first.inner_text().replace(",", "")
        except:
            pass

        # ---------- SELLER NAME (CORRECT) ----------
        try:
            merchant = page.locator("#merchant-info").inner_text()
            if "Sold by" in merchant:
                result["Seller Name"] = merchant.split("Sold by")[1].split(".")[0].strip()
        except:
            pass

        browser.close()
        return result
