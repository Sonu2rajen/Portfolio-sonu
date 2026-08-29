
╔══════════════════════════════════════════════════════════════════╗
║           SUPPRESSION MONITOR - COMPLETE SETUP GUIDE            ║
║                   Clicktech | Amazon.in                          ║
╚══════════════════════════════════════════════════════════════════╝

WHAT THIS TOOL DOES (End-to-End Automation):
─────────────────────────────────────────────
Every day at 7:00 AM, automatically:

  1. Reads your ASIN list (Clck-asins.xlsx)
  2. Opens each ASIN on Amazon.in and scrapes:
       - Availability (In stock / Currently unavailable / Error)
       - Asin Search (YES if correct page shown, NO if redirected)
       - Asin Reflect (ASIN shown in Additional Info on page)
  3. Filters out healthy in-stock ASINs
  4. Matches remaining ASINs with inventory (Sounce_Master_Monthly_Report.xlsx)
       - Removes ASINs not found in inventory
       - Removes ASINs with Sellable Qty < 30
  5. Compares with master file (Suppression_Sheet__1_.xlsx → Clicktech tab)
       - Finds NEW suppressions (not already in master)
  6. Updates master suppression file with new ASINs
  7. Sends email report to sonurajendran2@gmail.com with:
       - Summary stats
       - Table of newly suppressed ASINs
       - Full Excel report attached


═══════════════════════════════════════════════════════════════════
STEP 1: INSTALL PYTHON
═══════════════════════════════════════════════════════════════════

1. Download Python 3.11 from: https://python.org/downloads
2. During install → TICK ✅ "Add Python to PATH"
3. Click Install Now

Verify: Open Command Prompt and type:
   python --version
   (Should show Python 3.x.x)


═══════════════════════════════════════════════════════════════════
STEP 2: SETUP GMAIL APP PASSWORD
═══════════════════════════════════════════════════════════════════

Gmail now requires an "App Password" instead of your regular password.

How to generate:
  1. Go to: https://myaccount.google.com/security
  2. Make sure 2-Step Verification is ON
  3. Search for "App Passwords"
  4. Select app: "Mail" → Select device: "Windows Computer"
  5. Click Generate → Copy the 16-character password
  6. Open config.json → replace password with this App Password

⚠️ NOTE: If the current password in config.json doesn't work,
follow the steps above to generate an App Password.


═══════════════════════════════════════════════════════════════════
STEP 3: SETUP FOLDER STRUCTURE
═══════════════════════════════════════════════════════════════════

Your project folder: D:\admin\Desktop\Suppresstion-click\

├── main.py                        ← Main script
├── scraper.py                     ← Amazon scraper
├── processor.py                   ← Data processing
├── mailer.py                      ← Email sender
├── config.json                    ← Configuration
├── requirements.txt               ← Python packages
├── SETUP_SCHEDULER.bat            ← Run ONCE to set up auto-schedule
├── RUN_NOW.bat                    ← Run manually anytime
├── TEST_RUN.bat                   ← Test with 5 ASINs only
│
├── input\                         ← PUT DAILY FILES HERE
│   ├── Clck-asins.xlsx            ← ASIN list (update daily)
│   └── Sounce_Master_Monthly_Report.xlsx  ← Inventory report (update daily)
│
├── master\                        ← MASTER FILE LIVES HERE
│   └── Suppression_Sheet__1_.xlsx ← Universal suppression tracker
│
├── output\                        ← RESULTS SAVED HERE
│   └── Suppression_Clicktech_YYYY-MM-DD.xlsx
│
└── logs\                          ← LOG FILES
    └── suppression_YYYY-MM-DD.log


═══════════════════════════════════════════════════════════════════
STEP 4: FIRST TIME SETUP
═══════════════════════════════════════════════════════════════════

1. Copy all project files to: D:\admin\Desktop\Suppresstion-click\

2. Place your files:
   → Clck-asins.xlsx              → input\ folder
   → Sounce_Master_Monthly_Report.xlsx → input\ folder
   → Suppression_Sheet__1_.xlsx   → master\ folder

3. Right-click SETUP_SCHEDULER.bat → "Run as Administrator"
   (This installs packages + sets up daily 7 AM task)

4. Test it works: Double-click TEST_RUN.bat
   (Runs 5 ASINs, takes 2-3 mins, sends test email)


═══════════════════════════════════════════════════════════════════
STEP 5: DAILY OPERATIONS
═══════════════════════════════════════════════════════════════════

AUTOMATIC (Runs at 7:00 AM every day):
  - The tool runs automatically — you don't need to do anything!
  - Just make sure the PC is ON and files are in the input folder

MANUAL (Run anytime):
  - Double-click: RUN_NOW.bat

DAILY FILE UPDATE (do this before 7 AM):
  1. Replace input\Clck-asins.xlsx with today's ASIN file
  2. Replace input\Sounce_Master_Monthly_Report.xlsx with today's inventory

CHECK RESULTS:
  - Email arrives at: sonurajendran2@gmail.com
  - Excel report in: output\ folder
  - Logs in: logs\ folder


═══════════════════════════════════════════════════════════════════
CONFIGURATION (config.json)
═══════════════════════════════════════════════════════════════════

To change settings, open config.json in Notepad:

  "schedule_time"    → Change run time (default: "07:00")
  "min_sellable_qty" → Change minimum qty threshold (default: 30)
  "recipients"       → Add/remove email recipients
  "scraper_delay_min/max" → Adjust scraping speed (2-5 seconds default)


═══════════════════════════════════════════════════════════════════
TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════

❌ "Python not found"
   → Reinstall Python and check "Add to PATH"

❌ "Email authentication failed"
   → Generate Gmail App Password (Step 2 above)
   → Make sure 2-Step Verification is ON in Gmail

❌ "File not found" errors
   → Check files are placed in correct folders (Step 3)

❌ "ASIN column not found"
   → Make sure the Excel file has a column named 'ASIN'

❌ Scraper getting blocked by Amazon
   → Normal occasionally; the tool auto-retries 3 times
   → Try running at a different time
   → Logs will show which ASINs had errors

📋 LOGS location: D:\admin\Desktop\Suppresstion-click\logs\


═══════════════════════════════════════════════════════════════════
SUPPORT
═══════════════════════════════════════════════════════════════════

Sender Email  : connect.techetrade@gmail.com
Report sent to: sonurajendran2@gmail.com
Schedule      : Daily at 7:00 AM

Built for: Clicktech Suppression Monitoring | Amazon.in
