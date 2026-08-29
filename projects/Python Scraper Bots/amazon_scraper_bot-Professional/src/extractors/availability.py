import re

def extract_availability(page):
    """
    Returns availability text exactly as Amazon shows, with business rules applied.
    """

    try:
        availability_text = page.locator("#availability").inner_text().strip()
    except:
        return "Not Available"

    availability_lower = availability_text.lower()

    # --- Case 1: "Only X left in stock" (capture exact phrase) ---
    # Examples:
    # Only 1 left in stock.
    # Only one left in stock.
    # Only 2 left in stock.
    match = re.search(r"(only\s+.*?\s+left\s+in\s+stock)", availability_lower)
    if match:
        # Return original casing from page, not lowercased
        return availability_text.replace(".", "").strip()

    # --- Case 2: Temporarily unavailable ---
    if "temporarily unavailable" in availability_lower:
        return "Temporarily unavailable"

    # --- Case 3: Out of stock / Currently unavailable ---
    out_of_stock_phrases = [
        "currently unavailable",
        "out of stock",
        "not available"
    ]

    for phrase in out_of_stock_phrases:
        if phrase in availability_lower:
            return "Currently unavailable"

    # --- Case 4: Normal in-stock ---
    return "In stock"
