from playwright.sync_api import sync_playwright
from src.utils import random_delay

AMAZON_URL = "https://www.amazon.in/dp/{}"

class AmazonPage:

    def __init__(self, headless=False):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            slow_mo=500
        )
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def open_product(self, asin):
        self.page.goto(AMAZON_URL.format(asin), timeout=60000)

        try:
            # Product title = real product page
            self.page.wait_for_selector("#productTitle", timeout=30000)
        except:
            return False

        # Scroll to load dynamic sections
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        random_delay(2, 4)

        # Reject obvious error pages
        page_text = self.page.content().lower()
        if "sorry" in page_text and "we couldn't find" in page_text:
            return False

        return True



    def close(self):
        self.browser.close()
        self.playwright.stop()
