print(">>> ASIN EXTRACTOR v3 LOADED <<<")
def extract_asin_info(page, searched_asin):
    """
    Returns:
    asin_search (YES / NO)
    asin_reflect_value (actual ASIN found or blank)
    """

    asin_found = ""

    # -------- LOCATION 1: Detail Bullets --------
    try:
        items = page.locator("#detailBullets_feature_div li").all()
        for item in items:
            text = item.inner_text().strip()
            if text.startswith("ASIN"):
                asin_found = text.split(":")[-1].strip()
                break
    except:
        pass

    # -------- LOCATION 2: Product Details --------
    if not asin_found:
        try:
            rows = page.locator(
                "#productDetails_detailBullets_sections1 tr"
            ).all()
            for row in rows:
                key = row.locator("th").inner_text().strip()
                if key == "ASIN":
                    asin_found = row.locator("td").inner_text().strip()
                    break
        except:
            pass

    # -------- LOCATION 3: Technical Details (NEW) --------
    if not asin_found:
        try:
            rows = page.locator(
                "#productDetails_techSpec_section_1 tr"
            ).all()
            for row in rows:
                key = row.locator("th").inner_text().strip()
                if key == "ASIN":
                    asin_found = row.locator("td").inner_text().strip()
                    break
        except:
            pass

    # -------- FINAL DECISION --------
    if not asin_found:
        return "NO", ""

    if asin_found == searched_asin:
        return "YES", asin_found
    else:
        # redirected / replaced
        return "NO", asin_found
