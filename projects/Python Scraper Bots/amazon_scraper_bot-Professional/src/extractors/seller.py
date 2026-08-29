def extract_seller_name(page):
    """
    Extract seller name from 'Sold by' field on Amazon DP page.
    """

    # --- METHOD 1: Tabular Buy Box (MOST RELIABLE) ---
    try:
        rows = page.locator("#tabular-buybox tr").all()
        for row in rows:
            cells = row.locator("td").all()
            if len(cells) >= 2:
                label = cells[0].inner_text().strip().lower()
                value = cells[1].inner_text().strip()
                if label == "sold by":
                    return value
    except:
        pass

    # --- METHOD 2: Merchant info fallback ---
    try:
        text = page.locator("#merchant-info").inner_text()
        for line in text.split("\n"):
            if line.strip().lower().startswith("sold by"):
                return line.replace("Sold by", "").strip()
    except:
        pass

    return ""
