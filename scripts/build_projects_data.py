import os
import sys
import json
import zipfile
import re
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

PROJECTS_DIR = r"c:\Users\Z005955Y\OneDrive - Innomotics\Dokumente\mine\Portfolio-sonu\projects"
OUTPUT_JS = r"c:\Users\Z005955Y\OneDrive - Innomotics\Dokumente\mine\Portfolio-sonu\data\projects.js"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ══════════════════════════════════════════════
# EXACT 1:1 CATEGORY MAPPING (15 Categories)
# Physical folder → Portfolio display name
# ══════════════════════════════════════════════
CAT_DISPLAY = {
    "AI & ML Models":                      "AI & ML Models",
    "AI-Automation & Professional Bots":    "Automation & Bots",
    "Advanced Data Engineering":            "Advanced Data Engineering",
    "Docker & SQL EDA Pipelines":           "Docker & SQL Pipelines",
    "Excel Analytics & Dashboards":         "Excel Analytics",
    "Excel & Power Pivot Analysis":         "Excel & Power Pivot",
    "Full-Stack Application Development":   "Full-Stack Development",
    "Power BI & Snowflake":                 "Power BI & Snowflake",
    "Power BI & SQL EDA":                   "Power BI & SQL EDA",
    "Python EDA":                           "Python EDA",
    "Python Scraper Bots":                  "Python Scraper Bots",
    "SQL EDA & Advanced Data Handling":     "SQL EDA & Data Handling",
    "SQL, T-SQL & MySQL Operations":        "SQL, T-SQL & MySQL",
    "Tableau Analytics & Dashboard":        "Tableau Analytics",
    "Website Full-Stack Development":       "Website Development",
}

# Icon fallback per display category
ICON_MAP = {
    "AI & ML Models":           "assets/thumbnails/python.svg",
    "Automation & Bots":        "assets/thumbnails/automation.svg",
    "Advanced Data Engineering": "assets/thumbnails/cloud.svg",
    "Docker & SQL Pipelines":   "assets/thumbnails/cloud.svg",
    "Excel Analytics":          "assets/thumbnails/excel.svg",
    "Excel & Power Pivot":      "assets/thumbnails/excel.svg",
    "Full-Stack Development":   "assets/thumbnails/appdev.svg",
    "Power BI & Snowflake":     "assets/thumbnails/powerbi.svg",
    "Power BI & SQL EDA":       "assets/thumbnails/powerbi.svg",
    "Python EDA":               "assets/thumbnails/python.svg",
    "Python Scraper Bots":      "assets/thumbnails/python.svg",
    "SQL EDA & Data Handling":  "assets/thumbnails/sql.svg",
    "SQL, T-SQL & MySQL":       "assets/thumbnails/sql.svg",
    "Tableau Analytics":        "assets/thumbnails/tableau.svg",
    "Website Development":      "assets/thumbnails/appdev.svg",
}

# ── Home Page display order (priority) ──
DISPLAY_ORDER = [
    "Power BI & SQL EDA",
    "Power BI & Snowflake",
    "Tableau Analytics",
    "Excel Analytics",
    "Excel & Power Pivot",
    "Full-Stack Development",
    "SQL EDA & Data Handling",
    "SQL, T-SQL & MySQL",
    "Python EDA",
    "AI & ML Models",
    "Automation & Bots",
    "Python Scraper Bots",
    "Advanced Data Engineering",
    "Docker & SQL Pipelines",
    "Website Development",
]

# ══════════════════════════════════════════════
# PRESERVED NON-PROJECT DATA
# ══════════════════════════════════════════════

FLOATING_HERO_CARDS = [
    {"title": "DATA ANALYTICS & BI", "stack": "Power BI \u2022 SQL \u2022 Tableau \u2022 Advanced Excel", "positionClass": "hero-float-1"},
    {"title": "DATA ENGINEERING", "stack": "Python \u2022 ETL \u2022 Data Pipelines \u2022 SQL", "positionClass": "hero-float-2"},
    {"title": "AUTOMATION & AI", "stack": "Python Automation \u2022 VBA \u2022 AI-Assisted Workflows", "positionClass": "hero-float-3"},
    {"title": "INDUSTRIAL & BUSINESS ANALYTICS", "stack": "Operational Data \u2022 Supply Chain \u2022 Performance Analytics", "positionClass": "hero-float-4"},
    {"title": "APPLICATION & DATA PLATFORMS", "stack": "Flutter \u2022 Spring Boot \u2022 APIs \u2022 Data Platforms", "positionClass": "hero-float-5"},
]

ACHIEVEMENTS = [
    {"val": "~2 Yrs", "label": "Experience in BI & Analytics"},
    {"val": "75,670+", "label": "Records Validated (Global Governance)"},
    {"val": "130+", "label": "Enterprise Contracts Restructured"},
    {"val": "45+", "label": "Projects & Dashboards Shipped"},
    {"val": "96%+", "label": "Asset Data Visibility Achieved"},
]

EXPERIENCE = [
    {
        "role": "Executive Data Analyst & Customer Service Technical",
        "company": "Innomotics India Ltd.",
        "period": "Mar 2026 \u2013 Present",
        "location": "Mumbai, India",
        "highlights": [
            "Built a Contract Intelligence Dashboard in Power BI using SQL to query and restructure historical contract data across 130+ enterprise service contracts, cutting lookup time from 5\u201310 minutes to ~10 seconds.",
            "Cleansed and validated 75,670+ Installed Base records using SQL as one of two India-based analysts on a global Master Data Governance initiative, collaborating daily with Germany\u2019s data team to standardize the SIRIUS system.",
            "Designed an Installed Base Intelligence Dashboard covering 3,800+ industrial assets using SQL for data preparation and Power BI Star Schema modeling \u2014 cutting manual analysis by 70\u201380% with 96%+ trusted asset visibility.",
            "Built a Time Entries & Utilization Dashboard using SQL and Star Schema modeling on Dataverse-sourced data, cutting a half-day manual process to minutes.",
            "Investigated duplicate records, inactive tickets, and IBase inconsistencies using SQL and Python; built supporting SSIS/SSRS pipelines to load and clean Dynamics 365 data.",
            "Developed a QR-based asset management app (Flutter, Spring Boot, JWT, PostgreSQL, Docker, Kubernetes) digitizing access to records for 16,218 drives and 80,000+ documents.",
            "Coordinated with external service vendors on breakdown-visit and preventive maintenance scheduling, presenting findings to stakeholders across Germany and India.",
        ],
        "relatedProject": "installed-base-intelligence",
    },
    {
        "role": "Data Analyst | Data Platform Developer",
        "company": "Sounce Retail Pvt Ltd",
        "period": "Feb 2025 \u2013 Mar 2026",
        "location": "Mumbai, India",
        "highlights": [
            "Automated Daily Run Rate calculations via Excel VBA across 3,000+ SKUs, cutting processing time by 90% and giving procurement same-day restocking visibility.",
            "Built Power BI and Tableau dashboards tracking inventory, sales, pricing, and product performance across 3,000+ SKUs, turning multi-day manual analysis into minutes.",
            "Wrote SQL queries and built Python ETL pipelines consolidating multi-platform sales, pricing, and procurement data into automated monthly finance and margin/suppression reports.",
            "Ran pricing, margin, and product-suppression analysis across 6 marketplaces (Amazon, Flipkart, Shopify, Blinkit, Zepto, Nykaa) to flag profitability issues before sell-through was impacted.",
            "Queried customer behavior, conversion, and seasonality trends in SQL to identify high-value segments and cross-sell opportunities.",
            "Built a Python scraping bot pulling pricing, title, and category data from Amazon, Flipkart, Blinkit, Swiggy, and Nykaa product pages, cutting data collection from a full day to under an hour.",
        ],
        "relatedProject": "daily-run-rate-vba",
    },
    {
        "role": "Data Analytics Intern",
        "company": "Infotech",
        "period": "Jul 2024 \u2013 Sep 2024",
        "location": "Mumbai, India",
        "highlights": [
            "Engineered AI automation workflows and predictive data pipelines using Python, Scikit-learn, and OpenAI APIs.",
        ],
        "relatedProject": "resume-parser-bot",
    },
    {
        "role": "Web Development Intern",
        "company": "Unified Mentor Pvt Ltd",
        "period": "Jan 2024 \u2013 Feb 2024",
        "location": "Mumbai, India",
        "highlights": [
            "Developed responsive web application frontends and client-side components using React.js and REST APIs.",
        ],
        "relatedProject": None,
    },
]

EDUCATION = [
    {
        "degree": "Master of Computer Science (MSc)",
        "institution": "SIES College of Arts, Science & Commerce",
        "period": "2023 \u2013 2025",
        "grade": "CGPA 8.4 / 10",
        "details": "Advanced software engineering, database architectures, enterprise data modeling, machine learning fundamentals, and distributed system development.",
    },
    {
        "degree": "Bachelor of Computer Science (BSc)",
        "institution": "SIES College of Arts, Science & Commerce",
        "period": "2020 \u2013 2023",
        "grade": "CGPA 8.6 / 10",
        "details": "Computer science core foundations, object-oriented programming, data structures, algorithms, relational database design (SQL), and web technologies.",
    },
]

CERTIFICATIONS = [
    {"name": "Google Data Analytics Certificate", "issuer": "Google", "icon": "\U0001f393", "status": "Completed", "desc": "End-to-end data analysis methodology, data cleaning, SQL query optimization, R/Python visualization, and stakeholder communication."},
    {"name": "PL-300: Microsoft Power BI Data Analyst", "issuer": "Microsoft", "icon": "\U0001f4ca", "status": "In Progress", "desc": "Advanced data preparation, Star Schema modeling, DAX time intelligence, report design, security governance, and service workspace management."},
    {"name": "Python for Data Science", "issuer": "NPTEL", "icon": "\U0001f40d", "status": "Completed", "desc": "Python fundamentals for analytical processing, data wrangling with Pandas/NumPy, data visualization, and exploratory data analysis."},
    {"name": "SQL for Data Science", "issuer": "Coursera", "icon": "\U0001f5c3\ufe0f", "status": "Completed", "desc": "Relational database querying, multi-table joins, subqueries, CTEs, string manipulation, window functions, and data analysis."},
]

# ══════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════

def format_title(folder_name):
    """Clean folder name into human-readable title."""
    title = folder_name
    for suffix in ["-Professional", "_Professional"]:
        title = title.replace(suffix, "")
    title = title.replace("-Dashboard", " Dashboard").replace("_Dashboard", " Dashboard")
    title = title.replace("-", " ").replace("_", " ")
    words = title.split()
    upper_words = {"eda", "sql", "hr", "aws", "etl", "bi", "vba", "sku", "nlp", "ai", "ml", "api", "mysql", "tsql"}
    cleaned = []
    for w in words:
        if w.lower() in upper_words:
            cleaned.append(w.upper())
        elif w.lower() == "powerbi":
            cleaned.append("Power BI")
        else:
            cleaned.append(w.capitalize())
    return " ".join(cleaned)


# ══════════════════════════════════════════════
# GITHUB LINKS CONFIG LOADER
# ══════════════════════════════════════════════

GITHUB_LINKS_FILE = r"c:\Users\Z005955Y\OneDrive - Innomotics\Dokumente\mine\Portfolio-sonu\data\github_links.json"

def load_github_links():
    if os.path.exists(GITHUB_LINKS_FILE):
        try:
            with open(GITHUB_LINKS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"universal_github_url": "https://github.com/Sonu2rajen", "project_github_links": {}}

GITHUB_CONFIG = load_github_links()
UNIVERSAL_GITHUB_URL = GITHUB_CONFIG.get("universal_github_url", "https://github.com/Sonu2rajen")
PROJECT_GITHUB_LINKS = GITHUB_CONFIG.get("project_github_links", {})

def get_project_github_url(proj_id):
    return PROJECT_GITHUB_LINKS.get(proj_id, UNIVERSAL_GITHUB_URL)


def discover_project_media(proj_path):
    """
    Find all images and representative video file in a project folder.
    Strictly prioritizes dedicated Project_Images / Project-Images folders if present.
    """
    valid_exts = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
    image_files = []
    video_file = None

    # Check for direct Project_Images / Project-Images / Project Images folder first
    dedicated_img_dir = None
    if os.path.exists(proj_path):
        for item in os.listdir(proj_path):
            item_path = os.path.join(proj_path, item)
            if os.path.isdir(item_path) and item.lower() in ["project_images", "project-images", "project images"]:
                dedicated_img_dir = item_path
                break

    search_dirs = []
    if dedicated_img_dir:
        # Search ONLY inside dedicated Project_Images folder
        for root_dir, dirs, files in os.walk(dedicated_img_dir):
            search_dirs.append(root_dir)
    else:
        # Fallback to checking root and top-level screenshots/images folders
        search_dirs.append(proj_path)
        if os.path.exists(proj_path):
            for item in os.listdir(proj_path):
                item_path = os.path.join(proj_path, item)
                if os.path.isdir(item_path) and item.lower() in ["screenshots", "images", "img", "media"]:
                    search_dirs.append(item_path)

    seen_rel_paths = set()

    for sdir in search_dirs:
        try:
            entries = sorted(os.listdir(sdir))
        except Exception:
            continue

        for f in entries:
            fp = os.path.join(sdir, f)
            if os.path.isdir(fp):
                continue

            ext = os.path.splitext(f)[1].lower()
            rel_p = os.path.relpath(fp, PROJECT_ROOT).replace("\\", "/")

            if rel_p in seen_rel_paths:
                continue

            if ext in [".mp4", ".webm", ".mov", ".avi"] and not video_file:
                video_file = rel_p
                seen_rel_paths.add(rel_p)
            elif ext in valid_exts:
                if any(x in f.lower() for x in ["ic_launcher", "favicon", "appicon"]):
                    continue
                image_files.append(rel_p)
                seen_rel_paths.add(rel_p)

    return image_files[:20], video_file


def parse_docx_sections(doc_path):
    """Extract structured content from docx or plain text (.txt / .md) preserving headings and paragraphs."""
    if not doc_path or not os.path.exists(doc_path):
        return []

    # Check if text or markdown file
    if doc_path.lower().endswith((".txt", ".md")):
        try:
            with open(doc_path, "r", encoding="utf-8", errors="ignore") as tf:
                text_content = tf.read()
            lines = [l.strip() for l in text_content.split("\n") if l.strip()]
            sections = []
            current_heading = "OVERVIEW"
            current_lines = []
            for line in lines:
                if line.startswith("#") or line.isupper() and len(line) < 60:
                    if current_lines:
                        sections.append({"heading": current_heading, "content": current_lines})
                        current_lines = []
                    current_heading = line.lstrip("#").strip()
                else:
                    current_lines.append(line)
            if current_lines:
                sections.append({"heading": current_heading, "content": current_lines})
            return sections
        except Exception as e:
            print(f"  [WARN] Error reading text description {doc_path}: {e}")
            return []

    try:
        with zipfile.ZipFile(doc_path) as z:
            xml_content = z.read("word/document.xml")
        root = ET.fromstring(xml_content)

        sections = []
        current_heading = "OVERVIEW"
        current_lines = []

        for p in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
            texts = [n.text for n in p.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if n.text]
            p_text = "".join(texts).strip()
            if not p_text:
                continue

            is_heading = False
            pStyle = p.find(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pStyle")
            if pStyle is not None:
                val = pStyle.attrib.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val", "")
                if "heading" in val.lower():
                    is_heading = True

            if not is_heading and (p_text.isupper() or re.match(r"^\d+\.\s+[A-Z]", p_text)) and len(p_text) < 70 and not p_text.startswith("\u2714") and not p_text.startswith("\u2022"):
                is_heading = True

            if is_heading:
                if current_lines:
                    sections.append({"heading": current_heading, "content": current_lines})
                    current_lines = []
                current_heading = p_text
            else:
                current_lines.append(p_text)

        if current_lines:
            sections.append({"heading": current_heading, "content": current_lines})
        return sections
    except Exception as e:
        print(f"  [WARN] Error parsing {doc_path}: {e}")
        return []


def select_code_file(item_path):
    """Find ONE representative .py or .sql file — NOT for the SQL-TSQL special category."""
    py_files = []
    sql_files = []
    for root_dir, dirs, files in os.walk(item_path):
        skip = any(x in root_dir.lower() for x in ["venv", "node_modules", ".git", "__pycache__"])
        if skip:
            continue
        for f in files:
            fp = os.path.join(root_dir, f)
            if f.lower().endswith(".py") and not f.startswith("."):
                py_files.append(fp)
            elif f.lower().endswith(".sql") and not f.startswith("."):
                sql_files.append(fp)

    chosen = None
    lang = "python"

    if sql_files:
        sql_files.sort(key=lambda x: os.path.getsize(x), reverse=True)
        chosen = sql_files[0]
        lang = "sql"
    elif py_files:
        py_files.sort(key=lambda x: os.path.getsize(x))
        for p in py_files:
            if os.path.getsize(p) < 100000:
                chosen = p
                lang = "python"
                break

    if chosen:
        try:
            with open(chosen, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
            code = re.sub(r'(password|secret|api_key|token)\s*=\s*["\'][^"\']+["\']', r'\1 = "*****"', code, flags=re.IGNORECASE)
            lines = code.split("\n")
            if len(lines) > 300:
                code = "\n".join(lines[:300]) + "\n\n# ... [code truncated for display] ..."
            return {"filename": os.path.basename(chosen), "language": lang, "code": code}
        except Exception:
            return None
    return None


def discover_all_sql_files(folder_path):
    """For the SQL-TSQL-MYSQL special category: discover every .sql file with full contents."""
    sql_list = []
    for f in sorted(os.listdir(folder_path)):
        if f.lower().endswith(".sql"):
            fp = os.path.join(folder_path, f)
            try:
                with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                    code = fh.read()
                code = re.sub(r'(password|secret|api_key|token)\s*=\s*["\'][^"\']+["\']', r'\1 = "*****"', code, flags=re.IGNORECASE)
                sql_list.append({"filename": f, "language": "sql", "code": code})
            except Exception:
                pass
    return sql_list


# ══════════════════════════════════════════════
# MAIN BUILD
# ══════════════════════════════════════════════

def build_projects():
    projects_list = []

    for cat_folder in sorted(os.listdir(PROJECTS_DIR)):
        cat_path = os.path.join(PROJECTS_DIR, cat_folder)
        if not os.path.isdir(cat_path):
            continue

        display_cat = CAT_DISPLAY.get(cat_folder)
        if not display_cat:
            print(f"  [WARN] Unknown category folder: {cat_folder} — skipping")
            continue

        is_sql_tsql = (display_cat == "SQL, T-SQL & MySQL")

        # ── Special case: "SQL, T-SQL & MySQL Operations" ──
        # This folder contains .sql files directly (no project sub-folders).
        if is_sql_tsql:
            sql_files = discover_all_sql_files(cat_path)
            docx_path = None
            for f in os.listdir(cat_path):
                if f.lower().endswith(".docx") and "description" in f.lower():
                    docx_path = os.path.join(cat_path, f)
                    break
            docx_sections = parse_docx_sections(docx_path) if docx_path else []

            # Build description summary from docx
            desc_text = "Comprehensive SQL, T-SQL & MySQL operations reference with 18+ SQL scripts covering joins, window functions, subqueries, ranking, pivot tables, string/numeric/date functions, and TCL commands."
            if docx_sections:
                all_paras = []
                for s in docx_sections:
                    all_paras.extend(s["content"])
                desc_text = " ".join(all_paras[:3])
                if len(desc_text) > 280:
                    desc_text = desc_text[:280] + "..."

            proj_data = {
                "id": "sql-tsql-mysql-operations",
                "title": "SQL, T-SQL & MySQL Operations",
                "category": display_cat,
                "tier": "Project",
                "tools": ["SQL", "T-SQL", "MySQL"],
                "outcome": f"Comprehensive SQL reference with {len(sql_files)} SQL scripts.",
                "description": desc_text,
                "link": "#",
                "githubUrl": get_project_github_url("sql-tsql-mysql-operations"),
                "researchPaperUrl": None,
                "thumbnail": ICON_MAP.get(display_cat, "assets/thumbnails/sql.svg"),
                "images": [],
                "docxSections": docx_sections,
                "codeSnippet": None,
                "allSqlFiles": sql_files,
            }
            projects_list.append(proj_data)
            print(f"  [{display_cat}] SQL, T-SQL & MySQL Operations — {len(sql_files)} SQL files")
            continue

        # ── Special case: "Excel & Power Pivot Analysis" ──
        # This folder has Project_Images directly and a docx, but no project sub-folders.
        has_project_subfolders = False
        for item in os.listdir(cat_path):
            item_full = os.path.join(cat_path, item)
            if os.path.isdir(item_full) and item != "Project_Images":
                has_project_subfolders = True
                break

        if not has_project_subfolders:
            # Treat the category folder itself as a single project
            docx_path = None
            for f in os.listdir(cat_path):
                if f.lower().endswith(".docx") and "description" in f.lower():
                    docx_path = os.path.join(cat_path, f)
                    break

            docx_sections = parse_docx_sections(docx_path) if docx_path else []

            image_files, video_file = discover_project_media(cat_path)
            proj_id = re.sub(r"[^a-zA-Z0-9]", "-", cat_folder.lower()).strip("-")
            proj_id = re.sub(r"-+", "-", proj_id)
            thumbnail = image_files[0] if image_files else ICON_MAP.get(display_cat, "assets/thumbnails/excel.svg")

            desc_rel_path = os.path.relpath(docx_path, PROJECT_ROOT).replace("\\", "/") if docx_path else None

            proj_data = {
                "id": proj_id,
                "title": format_title(cat_folder),
                "category": display_cat,
                "tier": "Professional",
                "tools": [display_cat],
                "outcome": f"Delivered comprehensive {display_cat} analysis.",
                "description": desc_text,
                "link": "#",
                "githubUrl": get_project_github_url(proj_id),
                "researchPaperUrl": None,
                "docxFilePath": desc_rel_path,
                "thumbnail": thumbnail,
                "images": image_files,
                "docxSections": docx_sections,
                "codeSnippet": select_code_file(cat_path),
                "allSqlFiles": None,
            }
            projects_list.append(proj_data)
            print(f"  [{display_cat}] {proj_data['title']} (single-project category)")
            continue

        # ── Normal categories with project sub-folders ──
        for proj_folder in sorted(os.listdir(cat_path)):
            if proj_folder.startswith(".") or proj_folder.lower() in ["project_images", "project-images", "project images", "screenshots", "images", "img"]:
                continue
            proj_path = os.path.join(cat_path, proj_folder)
            if not os.path.isdir(proj_path):
                continue

            proj_id = re.sub(r"[^a-zA-Z0-9]", "-", proj_folder.lower()).strip("-")
            title = format_title(proj_folder)
            tier = "Professional" if any(kw in proj_folder.lower() for kw in ["professional", "sounce", "ibase", "innomotics"]) else "Project"

            # Find Description file (.docx, .txt, or .md)
            docx_path = None
            for root_dir, dirs, files in os.walk(proj_path):
                for f in files:
                    if f.lower().endswith((".docx", ".txt", ".md")) and ("description" in f.lower() or "readme" in f.lower()):
                        docx_path = os.path.join(root_dir, f)
                        break
                if docx_path:
                    break

            docx_rel_path = None
            if docx_path:
                docx_rel_path = os.path.relpath(docx_path, PROJECT_ROOT).replace("\\", "/")

            docx_sections = parse_docx_sections(docx_path) if docx_path else []
            image_files, video_file = discover_project_media(proj_path)
            fallback_icon = ICON_MAP.get(display_cat, "assets/thumbnails/powerbi.svg")
            thumbnail = image_files[0] if image_files else fallback_icon

            # Description summary
            desc_text = f"Comprehensive {display_cat} project."
            if docx_sections:
                all_paras = []
                for s in docx_sections:
                    all_paras.extend(s["content"])
                desc_text = " ".join(all_paras[:3])
                if len(desc_text) > 280:
                    desc_text = desc_text[:280] + "..."

            # Tools inference
            tools = [display_cat]
            lower_folder = proj_folder.lower()
            if "sql" in lower_folder: tools.append("SQL")
            if "python" in lower_folder or "bot" in lower_folder or "scrapper" in lower_folder: tools.append("Python")
            if "excel" in lower_folder or "vba" in lower_folder: tools.append("Excel")
            if "powerbi" in lower_folder or "power-bi" in lower_folder: tools.append("Power BI")
            if "tableau" in lower_folder: tools.append("Tableau")
            if "docker" in lower_folder: tools.append("Docker")
            if "snowflake" in lower_folder: tools.append("Snowflake")
            tools = list(dict.fromkeys(tools))

            code_snippet = select_code_file(proj_path)

            proj_data = {
                "id": proj_id,
                "title": title,
                "category": display_cat,
                "tier": tier,
                "tools": tools,
                "outcome": f"Delivered comprehensive {display_cat} project.",
                "description": desc_text,
                "link": "#",
                "githubUrl": get_project_github_url(proj_id),
                "researchPaperUrl": None,
                "docxFilePath": docx_rel_path,
                "video": video_file,
                "thumbnail": thumbnail,
                "images": image_files,
                "docxSections": docx_sections,
                "codeSnippet": code_snippet,
                "allSqlFiles": None,
            }
            projects_list.append(proj_data)
            print(f"  [{display_cat}] {title} | DOCX: {bool(docx_path)} | Images: {len(image_files)} | Video: {bool(video_file)} | Code: {bool(code_snippet)}")

    # ── Interleaved Sorting: 2 projects per category first (image-filled first) ──
    cat_groups = {c: [] for c in DISPLAY_ORDER}
    for p in projects_list:
        cat = p["category"]
        if cat in cat_groups:
            cat_groups[cat].append(p)

    # Sort each group so projects with images come first
    for cat in cat_groups:
        cat_groups[cat].sort(key=lambda p: (0 if (p.get("images") or p.get("allSqlFiles")) else 1, p["title"]))

    final_projects_list = []
    # Round 1: Take up to 2 projects from each category
    for cat in DISPLAY_ORDER:
        group = cat_groups[cat]
        final_projects_list.extend(group[:2])

    # Round 2: Append remaining projects
    for cat in DISPLAY_ORDER:
        group = cat_groups[cat]
        if len(group) > 2:
            final_projects_list.extend(group[2:])

    projects_list = final_projects_list

    # ── Build CATEGORIES list (All + 15 individual) ──
    categories = ["All"]
    for cat_name in DISPLAY_ORDER:
        if any(p["category"] == cat_name for p in projects_list):
            categories.append(cat_name)

    print(f"\nTotal projects: {len(projects_list)}")
    print(f"Categories: {len(categories) - 1} + All")

    # ── Generate JS output ──
    js = f"""// ──────────────────────────────────────────────
// Sonu Rajendran — Portfolio Project Data System
// Auto-generated by scripts/build_projects_data.py
// ──────────────────────────────────────────────

const FLOATING_HERO_CARDS = {json.dumps(FLOATING_HERO_CARDS, indent=2, ensure_ascii=False)};

const ACHIEVEMENTS = {json.dumps(ACHIEVEMENTS, indent=2, ensure_ascii=False)};

const CATEGORIES = {json.dumps(categories, indent=2, ensure_ascii=False)};

const EXPERIENCE = {json.dumps(EXPERIENCE, indent=2, ensure_ascii=False)};

const EDUCATION = {json.dumps(EDUCATION, indent=2, ensure_ascii=False)};

const CERTIFICATIONS = {json.dumps(CERTIFICATIONS, indent=2, ensure_ascii=False)};

const PROJECTS = {json.dumps(projects_list, indent=2, ensure_ascii=False)};
"""

    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write(js)

    print(f"Wrote {OUTPUT_JS} ({len(js):,} bytes)")


if __name__ == "__main__":
    build_projects()
