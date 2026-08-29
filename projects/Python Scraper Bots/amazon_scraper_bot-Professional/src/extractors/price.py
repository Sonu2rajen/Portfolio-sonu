import re

def extract_price(page):
    """
    Returns numeric price only (no dots, commas, or text)
    """

    selectors = [
        "span.a-price-whole",
        "#priceblock_ourprice",
        "#priceblock_dealprice",
        "#priceblock_saleprice"
    ]

    for selector in selectors:
        try:
            loc = page.locator(selector)
            if loc.count():
                raw = loc.first.inner_text()

                # Keep digits only
                digits = re.findall(r"\d+", raw)
                if digits:
                    return "".join(digits)
        except:
            pass

    return ""
