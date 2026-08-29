"""
SUPPRESSION MONITOR - MAIN ORCHESTRATOR
=========================================
Clicktech | Amazon.in
Runs daily at scheduled time
Flow:
  1. Read ASINs from input file
  2. Scrape each ASIN from Amazon.in
  3. Process suppression logic (filter, vlookup, qty check)
  4. Find new suppressions vs master file
  5. Update master file
  6. Send email report
"""

import os
import sys
import json
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path

# ─── Setup paths ─────────────────────────────
BASE_DIR = Path(__file__).parent

def load_config():
    with open(BASE_DIR / "config.json", "r") as f:
        return json.load(f)

def setup_logging(log_dir):
    """Setup file + console logging"""
    os.makedirs(log_dir, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"suppression_{today}.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def setup_folders(config):
    """Create all required folders"""
    for key, path in config['folders'].items():
        os.makedirs(path, exist_ok=True)

def get_input_file(input_folder, filename):
    """Find the ASIN input file"""
    path = os.path.join(input_folder, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"ASIN input file not found: {path}\n"
            f"Please place '{filename}' in the input folder:\n{input_folder}"
        )
    return path

def get_inventory_file(input_folder, filename):
    """Find the inventory report file"""
    path = os.path.join(input_folder, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Inventory file not found: {path}\n"
            f"Please place '{filename}' in the input folder:\n{input_folder}"
        )
    return path

def get_master_file(master_folder, filename):
    """Find the master suppression file"""
    path = os.path.join(master_folder, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Master suppression file not found: {path}\n"
            f"Please place '{filename}' in the master folder:\n{master_folder}"
        )
    return path

def read_asin_list(asin_file_path):
    """Read ASINs from input Excel file"""
    df = pd.read_excel(asin_file_path)

    # Find the ASIN column (flexible naming)
    asin_col = None
    for col in df.columns:
        if 'asin' in col.lower():
            asin_col = col
            break

    if asin_col is None:
        # Assume first column
        asin_col = df.columns[0]

    asins = df[asin_col].dropna().astype(str).str.strip().tolist()
    asins = [a for a in asins if a and a != 'nan' and len(a) == 10]
    return asins


# ─── MAIN RUN FUNCTION ───────────────────────
def run(config=None, test_mode=False):
    """
    Main pipeline runner
    test_mode=True: only scrapes first 5 ASINs (for testing)
    """
    if config is None:
        config = load_config()

    logger = setup_logging(config['folders']['logs'])
    logger.info("=" * 60)
    logger.info(f"  SUPPRESSION MONITOR STARTED - {config['settings']['brand']}")
    logger.info(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    logger.info("=" * 60)

    try:
        # Setup folders
        setup_folders(config)

        # ── Locate files ──────────────────────
        asin_file    = get_input_file(config['folders']['input'], config['files']['asin_input'])
        inv_file     = get_inventory_file(config['folders']['input'], config['files']['inventory_report'])
        master_file  = get_master_file(config['folders']['master'], config['files']['master_suppression'])
        master_sheet = config['files']['master_sheet_name']

        logger.info(f"ASIN file    : {asin_file}")
        logger.info(f"Inventory    : {inv_file}")
        logger.info(f"Master file  : {master_file}")

        # ── Read ASINs ────────────────────────
        asin_list = read_asin_list(asin_file)
        logger.info(f"Loaded {len(asin_list)} ASINs to scrape")

        if test_mode:
            asin_list = asin_list[:5]
            logger.info(f"TEST MODE: Only scraping first 5 ASINs")

        # ── Scrape Amazon ────────────────────
        from scraper import scrape_all_asins

        def progress_cb(current, total, asin, result):
            pct = (current / total) * 100
            if current % 10 == 0:
                logger.info(f"Progress: {current}/{total} ({pct:.1f}%)")

        bot_results = scrape_all_asins(
            asin_list,
            delay_min=config['settings']['scraper_delay_min'],
            delay_max=config['settings']['scraper_delay_max'],
            retries=config['settings']['scraper_retries'],
            progress_callback=progress_cb
        )

        # ── Save raw scrape output immediately ──
        today_str = datetime.now().strftime("%Y-%m-%d")
        output_filename = f"Suppression_{config['settings']['brand']}_{today_str}.xlsx"
        output_path = os.path.join(config['folders']['output'], output_filename)

        # ── Run processing pipeline ───────────
        from processor import run_pipeline

        df_final, summary = run_pipeline(
            bot_results=bot_results,
            inventory_path=inv_file,
            master_path=master_file,
            master_sheet=master_sheet,
            output_path=output_path,
            min_qty=config['settings']['min_sellable_qty']
        )

        # ── Send email ────────────────────────
        from mailer import send_email

        email_sent = send_email(
            config=config,
            df_new_suppressions=df_final,
            summary=summary,
            attachment_path=output_path,
            brand=config['settings']['brand']
        )

        if email_sent:
            logger.info("✅ Email report sent successfully!")
        else:
            logger.warning("⚠️ Email sending failed — check logs for details")

        logger.info("=" * 60)
        logger.info("  SUPPRESSION MONITOR COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        return True

    except FileNotFoundError as e:
        logger.error(f"❌ FILE NOT FOUND ERROR:\n{e}")
        logger.error("Please check the input folder and try again.")
        return False

    except Exception as e:
        logger.exception(f"❌ UNEXPECTED ERROR: {e}")
        return False


# ─── ENTRY POINT ────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Clicktech Suppression Monitor')
    parser.add_argument('--test', action='store_true', help='Run in test mode (5 ASINs only)')
    args = parser.parse_args()
    run(test_mode=args.test)
