// ──────────────────────────────────────────────
// Sonu Rajendran — Portfolio Project Data System
// Data-driven single source of truth for:
// 1. Hero Achievements Highlights Bar
// 2. Main Projects Grid (Card Preview Slider)
// 3. Dedicated Case Study Pages (Media Carousel + Deep Dive)
// ──────────────────────────────────────────────

const ACHIEVEMENTS = [
  { val: "~2 Yrs", label: "Experience in BI & Analytics" },
  { val: "75,670+", label: "Records Validated (Global Governance)" },
  { val: "130+", label: "Service Contracts Restructured" },
  { val: "45+", label: "Projects & Dashboards Shipped" }
];

const PROJECTS = [

  // ═══════════════ POWER BI ═══════════════

  {
    id: "installed-base-intelligence",
    title: "Installed Base Intelligence Dashboard",
    category: "Power BI",
    tier: "Professional",
    tools: ["Power BI", "SQL", "Star Schema", "DAX", "Power Query"],
    outcome: "96%+ trusted asset visibility across 3,800+ assets — cut manual analysis by 70–80%.",
    description: "Designed a Star Schema model in Power BI to resolve table relationship conflicts across 3,800+ installed industrial assets, providing full post-sales lifecycle intelligence across heavy industries in India.",
    company: "Innomotics India Ltd.",
    link: "#",
    thumbnail: "assets/thumbnails/powerbi.svg",
    
    // Project Media Assets
    images: [
      "assets/projects/ibase/Screenshot 2026-08-17 112003.png",
      "assets/projects/ibase/Screenshot 2026-08-17 112037.png",
      "assets/projects/ibase/Screenshot 2026-08-17 112044.png",
      "assets/projects/ibase/Screenshot 2026-08-17 112058.png",
      "assets/projects/ibase/Screenshot 2026-08-17 112109.png",
      "assets/projects/ibase/Screenshot 2026-08-17 112120.png"
    ],
    video: "assets/projects/ibase/Ibase-Dashboard_Video.mp4",

    // Links & Resources
    githubUrl: "",
    researchPdf: "", // Placeholder for future PDF

    // Full Case Study Content
    objective: "Digitize and unify India's installed industrial asset footprint across 3,800+ heavy equipment units (motors, drives, compressors, turbines) to transform post-sales service planning and executive decision-making.",
    requirements: "Consolidate fragmented asset registers across steel, cement, oil & gas, and power sectors. Standardize equipment identifiers (UEID, MLFB), resolve table relationship conflicts in Power BI, and build multi-page analytical views for executive leadership and operational service teams.",
    purpose: "Enable post-sales lifecycle intelligence, track asset population growth trends, identify high-exposure customer accounts, and pinpoint unverified or preliminary installed base records across India.",
    problem: "Service engineers and schedulers previously had to manually cross-reference historical contract records, disparate spreadsheets, and disconnected legacy databases to verify installed asset details. This manual lookup took 5–10 minutes per request, created operational bottlenecks, and left over 25% of installed base records unverified.",
    approach: "Utilized SQL for deep data cleansing, deduplication, and restructuring of master asset tables. Engineered a Power BI Star Schema data model separating fact tables (unit installations) from dimension tables (Customer, Product MLFB, Geography, Time). Authored advanced DAX measures for active footprint, data quality maturity ratios, and growth trajectory.",
    solution: "Delivered a comprehensive 4-page enterprise Power BI dashboard:\n• Page 1: Executive Asset Footprint & Data Quality KPIs\n• Page 2: Product Portfolio Intelligence & MLFB Family Analysis\n• Page 3: Customer & Site Geographic Distribution\n• Page 4: Installed Base Lifecycle Growth & Verification Drill-Down",
    result: "Achieved 96%+ trusted asset visibility across 3,800+ active industrial assets, reduced manual data analysis time by 70–80%, and gave regional service leadership instant clarity on key strategic accounts (ArcelorMittal Nippon Steel, Reliance, JSW Steel, NTPC, IOCL).",
    technicalDetails: [
      "SQL data cleansing & restructuring across 3,800+ unique equipment records (UEID primary key).",
      "Star Schema dimensional modeling in Power BI Desktop to eliminate circular relationships.",
      "DAX measures for Active/Verified vs. Preliminary status distribution ratios.",
      "Power Query M transformations for dynamic site and customer name standardization.",
      "Integration readiness for SIRIUS master data governance workflows."
    ]
  },
  {
    id: "contract-intelligence-dashboard",
    title: "Contract Intelligence Dashboard",
    category: "Power BI",
    tier: "Professional",
    tools: ["Power BI", "SQL", "DAX", "Star Schema", "Power Query"],
    outcome: "Cut contract lookup time from 5–10 min to ~10 seconds across 130+ enterprise contracts.",
    description: "Built a Power BI dashboard using SQL to query and restructure historical contract data across 130+ enterprise service contracts at Innomotics. Enabled instant contract insights for engineer scheduling.",
    company: "Innomotics India Ltd.",
    link: "#",
    thumbnail: "assets/thumbnails/powerbi.svg",
    images: [],
    video: "",
    githubUrl: "",
    researchPdf: "",
    objective: "Streamline service engineer dispatching and contract entitlement verification across enterprise service contracts.",
    requirements: "Unify historical service contract terms, SLA commitments, expiry dates, and covered equipment lines into an interactive dashboard.",
    purpose: "Provide service schedulers with immediate clarity on active contract coverage and SLA obligations.",
    problem: "Service schedulers spent 5–10 minutes digging through physical PDFs and disconnected network drives to verify contract terms before scheduling service visits.",
    approach: "Queried and restructured contract data in SQL, built clean relational relationships in Power BI, and implemented DAX measures for entitlement and expiring contract alerts.",
    solution: "Interactive Contract Intelligence Dashboard featuring contract lookup search, SLA tracking, and expiry notifications.",
    result: "Reduced contract lookup time to ~10 seconds for 130+ enterprise service contracts, speeding up engineer scheduling and eliminating SLA breach risks.",
    technicalDetails: ["SQL query optimization", "Power BI Star Schema modeling", "DAX time intelligence", "SLA tracking logic"]
  },
  {
    id: "time-entries-utilization",
    title: "Time Entries & Utilization Dashboard",
    category: "Power BI",
    tier: "Professional",
    tools: ["Power BI", "SQL", "Star Schema", "Dataverse"],
    outcome: "Cut a half-day manual productivity reporting process to minutes.",
    description: "Built on Dataverse-sourced data with Star Schema modeling, giving management direct visibility into productivity and site-visit utilization.",
    company: "Innomotics India Ltd.",
    link: "#",
    thumbnail: "assets/thumbnails/powerbi.svg",
    images: [],
    video: "",
    githubUrl: "",
    researchPdf: "",
    objective: "Provide executive management with real-time visibility into engineer field utilization and billable hours.",
    requirements: "Integrate Dataverse time logs with engineer rosters and site-visit schedules.",
    purpose: "Optimize resource allocation across nationwide industrial service projects.",
    problem: "Manual spreadsheet aggregation required a half-day every week to report engineer utilization.",
    approach: "Connected Power BI directly to Dataverse tables, modeled time entries into a star schema, and designed utilization percentage KPIs.",
    solution: "Automated utilization dashboard updated dynamically with daily field log sync.",
    result: "Reduced weekly reporting time from a half-day to under 5 minutes.",
    technicalDetails: ["Dataverse REST API connector", "Power BI Star Schema", "DAX utilization metrics"]
  },
  {
    id: "sales-tracker-dashboard",
    title: "Sales Performance Tracker",
    category: "Power BI",
    tier: "Professional",
    tools: ["Power BI", "DAX", "Power Query"],
    outcome: "Identified high- and low-performing products across 3,000+ SKUs.",
    description: "Designed interactive sales dashboards tracking inventory, pricing, and product performance across multiple e-commerce marketplaces.",
    company: "Sounce Retail",
    link: "#",
    thumbnail: "assets/thumbnails/powerbi.svg",
    images: [],
    video: "",
    githubUrl: "",
    researchPdf: "",
    objective: "Track multi-marketplace sales metrics and identify growth drivers across 3,000+ SKUs.",
    requirements: "Consolidate sales data from Amazon, Flipkart, Shopify, and quick-commerce channels.",
    purpose: "Guide procurement and inventory reordering strategies.",
    problem: "Siloed marketplace data prevented unified visibility into daily sales velocity.",
    approach: "Built automated data ingestion pipelines feeding a central Power BI model with custom DAX rank and trend measures.",
    solution: "Multi-channel executive sales tracker with interactive category and SKU drill-downs.",
    result: "Enabled immediate identification of top-performing SKUs and underperforming inventory.",
    technicalDetails: ["Power Query ETL", "Multi-fact table modeling", "DAX dynamic ranking"]
  },
  {
    id: "inventory-analytics-dashboard",
    title: "Inventory Analytics Dashboard",
    category: "Power BI",
    tier: "Professional",
    tools: ["Power BI", "SQL", "DAX"],
    outcome: "Real-time inventory tracking across 3,000+ SKUs and 6 marketplaces.",
    description: "Consolidated multi-platform inventory data into a single Power BI view for procurement and operations teams.",
    company: "Sounce Retail",
    link: "#",
    thumbnail: "assets/thumbnails/powerbi.svg",
    images: [],
    video: "",
    githubUrl: "",
    researchPdf: "",
    objective: "Eliminate stockouts and overstocking by unifying inventory levels across fulfillment hubs.",
    requirements: "Daily inventory updates across Amazon FBA, seller hubs, and regional warehouses.",
    purpose: "Maintain optimal stock buffer levels for fast-moving consumer tech accessories.",
    problem: "Stockouts caused lost buy-box positions on major e-commerce platforms.",
    approach: "Modeled inventory aging, turnover rates, and reorder threshold DAX measures.",
    solution: "Real-time Inventory Analytics Dashboard with automated low-stock triggers.",
    result: "Improved inventory turnover rate and eliminated stockout penalties on major platforms.",
    technicalDetails: ["Inventory reorder point modeling", "DAX stock aging", "Automated refresh schedules"]
  },
  {
    id: "pricing-margin-dashboard",
    title: "Pricing & Margin Analysis Dashboard",
    category: "Power BI",
    tier: "Professional",
    tools: ["Power BI", "SQL", "DAX"],
    outcome: "Flagged profitability issues across 6 marketplaces before they affected sell-through.",
    description: "Tracked pricing, margins, and product suppression across Amazon, Flipkart, Shopify, Blinkit, Zepto, and Nykaa.",
    company: "Sounce Retail",
    link: "#",
    thumbnail: "assets/thumbnails/powerbi.svg",
    images: [],
    video: "",
    githubUrl: "",
    researchPdf: "",
    objective: "Monitor net margin after marketplace commission, logistics fees, and ad spends.",
    requirements: "Calculate real-time SKU margin variations across 6 marketplaces.",
    purpose: "Prevent margin erosion from competitive price changes and platform commission updates.",
    problem: "Unnoticed price suppressions and ad cost surges lowered SKU net profitability.",
    approach: "Constructed margin waterfall models in DAX factoring in commissions, shipping, taxes, and ad spend per SKU.",
    solution: "Margin & Price Suppression Radar Dashboard highlighting margin-negative SKUs.",
    result: "Saved significant margin by catching pricing suppressions and ad overspends early.",
    technicalDetails: ["Waterfall DAX modeling", "Margin calculation formulas", "Marketplace API integration"]
  },

  // ═══════════════ EXCEL (VBA & MACROS) ═══════════════

  {
    id: "daily-run-rate-vba",
    title: "Daily Run Rate VBA Automation",
    category: "Excel",
    tier: "Professional",
    tools: ["Excel", "VBA", "Pivot Tables", "Macros"],
    outcome: "Cut processing time by 90% across 3,000+ SKUs — same-day restocking visibility.",
    description: "Automated daily run-rate calculations via Excel VBA macros, replacing multi-hour manual processes for the procurement team.",
    company: "Sounce Retail",
    link: "#",
    thumbnail: "assets/thumbnails/excel.svg",
    images: [],
    video: "",
    githubUrl: "",
    researchPdf: "",
    objective: "Automate daily demand forecasting and restocking calculations for 3,000+ e-commerce SKUs.",
    requirements: "Process raw multi-channel export files into daily run rates with a single button click.",
    purpose: "Provide procurement with immediate purchase order quantities every morning.",
    problem: "Manual spreadsheet calculation took 2-3 hours daily, delaying purchase orders.",
    approach: "Wrote modular VBA script automating data import, string parsing, pivot creation, and run-rate formulas.",
    solution: "One-click Excel VBA tool with automated error handling and summary reports.",
    result: "Cut processing time by 90%, enabling same-day purchase order dispatch.",
    technicalDetails: ["Excel VBA scripting", "Automated PivotTable generation", "Dynamic array formulas"]
  },

  // ═══════════════ SQL & DATABASES ═══════════════

  {
    id: "sql-eda-customer-behavior",
    title: "Customer Behavior EDA — SQL",
    category: "SQL",
    tier: "Project",
    tools: ["SQL", "CTEs", "Window Functions", "Aggregations"],
    outcome: "Identified high-value customer segments and conversion trends from raw transaction data.",
    description: "Exploratory data analysis on customer behavior data using advanced SQL queries, CTEs, and window functions.",
    link: "#",
    thumbnail: "assets/thumbnails/sql.svg",
    images: [],
    video: "",
    githubUrl: "",
    researchPdf: "",
    objective: "Analyze customer purchase frequency, recency, and monetary value (RFM) from raw transactional database tables.",
    requirements: "Write optimized SQL queries utilizing Common Table Expressions (CTEs) and window functions.",
    purpose: "Discover customer retention dynamics and identify churn risk patterns.",
    problem: "Large transactional table contained millions of rows requiring structured aggregations.",
    approach: "Designed multi-stage CTEs computing customer RFM scores, cohort retention rates, and moving average spend.",
    solution: "Comprehensive SQL query library for customer intelligence analysis.",
    result: "Uncovered key high-value segments contributing to 70% of repeat revenue.",
    technicalDetails: ["SQL CTEs", "Window functions (NTILE, LAG, ROW_NUMBER)", "Query optimization"]
  },

  // ═══════════════ TABLEAU ═══════════════

  {
    id: "tableau-sales-dashboard",
    title: "Sales Performance Dashboard",
    category: "Tableau",
    tier: "Project",
    tools: ["Tableau", "SQL"],
    outcome: "Interactive sales visualization with drill-down by region and product.",
    description: "Built interactive Tableau dashboards for sales performance analysis with geographic drill-downs.",
    link: "#",
    thumbnail: "assets/thumbnails/tableau.svg",
    images: [],
    video: "",
    githubUrl: "",
    researchPdf: "",
    objective: "Create geographic and product-line sales visualizations for executive presentations.",
    requirements: "Interactive Tableau dashboard with parameters, action filters, and custom calculated fields.",
    purpose: "Provide regional sales managers with intuitive performance benchmarks.",
    problem: "Static PowerPoint decks failed to provide interactive drill-downs during leadership reviews.",
    approach: "Cleaned data in SQL, extracted data engine hyper files, and constructed interactive Tableau worksheets.",
    solution: "Executive Tableau dashboard with interactive choropleth map and product category filters.",
    result: "Streamlined monthly regional sales review meetings.",
    technicalDetails: ["Tableau Calculated Fields", "LOD Expressions", "Interactive Action Filters"]
  },

  // ═══════════════ PYTHON ANALYTICS ═══════════════

  {
    id: "amazon-scraper-python",
    title: "Amazon Product Data Scraper Bot",
    category: "Python",
    tier: "Professional",
    tools: ["Python", "BeautifulSoup", "Requests", "Pandas"],
    outcome: "Cut data collection from a full day to under an hour.",
    description: "Built a scraping bot pulling pricing, title, and category data from Amazon, Flipkart, Blinkit, Swiggy, and Nykaa product pages.",
    company: "Sounce Retail",
    link: "#",
    thumbnail: "assets/thumbnails/python.svg",
    images: [],
    video: "",
    githubUrl: "",
    researchPdf: "",
    objective: "Automate competitive price tracking and product listing monitoring across e-commerce platforms.",
    requirements: "Extract product pricing, titles, ratings, and buy-box status automatically.",
    purpose: "Feed pricing intelligence models for margin and price suppression analysis.",
    problem: "Manual checking of competitor prices took full team days and missed fast price changes.",
    approach: "Built Python scraping bot using Requests, BeautifulSoup, user-agent rotation, and Pandas export pipelines.",
    solution: "Scheduled automated scraping script outputting clean CSV data daily.",
    result: "Reduced data collection time from a full day to under 45 minutes.",
    technicalDetails: ["Python BeautifulSoup", "Requests headers rotation", "Pandas data wrangling"]
  },

  // ═══════════════ APPLICATION DEVELOPMENT ═══════════════

  {
    id: "ibase-asset-management-app",
    title: "QR-Based Industrial Asset Management App",
    category: "App Dev",
    tier: "Professional",
    tools: ["Flutter", "Spring Boot", "JWT", "PostgreSQL", "Docker", "Kubernetes"],
    outcome: "Digitized access to 16,218 drives and 80,000+ documents — in ACP production validation.",
    description: "Developed a full-stack QR-based asset management application with Flutter frontend, Spring Boot API, JWT authentication, PostgreSQL database, containerized with Docker and orchestrated on Kubernetes.",
    company: "Innomotics India Ltd.",
    link: "#",
    thumbnail: "assets/thumbnails/appdev.svg",
    images: [],
    video: "",
    githubUrl: "",
    researchPdf: "",
    objective: "Enable field engineers to instantly scan physical asset QR tags to pull technical specs, manual PDFs, and maintenance history.",
    requirements: "Cross-platform mobile UI (Flutter), secure REST API (Spring Boot + JWT), scalable database (PostgreSQL), and containerized deployment (Docker + K8s).",
    purpose: "Eliminate manual paperwork during field maintenance visits across 16,218 installed drives.",
    problem: "Field engineers had to carry physical binders or call headquarters to access wiring diagrams and motor drive technical specs.",
    approach: "Architected a microservices backend with Spring Boot, dynamic QR scanning in Flutter, and container orchestration with Kubernetes.",
    solution: "Production-ready mobile & web application delivering instant asset record lookup on tag scan.",
    result: "Digitized access to 16,218 drives and 80,000+ technical documents; currently undergoing ACP cyber-security validation.",
    technicalDetails: ["Flutter UI", "Spring Boot REST API", "JWT Security", "PostgreSQL", "Docker Containerization", "Kubernetes Orchestration"]
  },

  // ═══════════════ AUTOMATION & BOTS ═══════════════

  {
    id: "resume-parser-bot",
    title: "AI Resume Parser Bot",
    category: "Automation",
    tier: "Project",
    tools: ["Python", "OpenAI API", "PyPDF2", "JSON"],
    outcome: "Automated resume parsing and structured JSON extraction from unstructured PDFs.",
    description: "Built an AI-powered resume parser using Python and OpenAI APIs to extract structured data from PDF resumes.",
    link: "#",
    thumbnail: "assets/thumbnails/automation.svg",
    images: [],
    video: "",
    githubUrl: "",
    researchPdf: "",
    objective: "Extract candidate contact details, skills, experience, and education into structured JSON from PDF resumes.",
    requirements: "Python backend handling PDF text extraction and structured LLM prompt engineering.",
    purpose: "Streamline candidate evaluation workflows.",
    problem: "Manual screening of hundreds of candidate PDFs was slow and prone to oversight.",
    approach: "Used PyPDF2 for text extraction, combined with OpenAI API JSON schema mode for structured output generation.",
    solution: "Automated Python CLI tool for batch resume processing.",
    result: "Processed 100+ resumes in seconds with high extraction accuracy.",
    technicalDetails: ["Python PyPDF2", "OpenAI API Structured Output", "JSON schema validation"]
  },

  // ═══════════════ CLOUD & DATA ENGINEERING ═══════════════

  {
    id: "aws-redshift-etl",
    title: "AWS Redshift ETL Pipeline",
    category: "Cloud/ETL",
    tier: "Project",
    tools: ["AWS Redshift", "Python", "ETL", "S3", "Boto3"],
    outcome: "Built end-to-end cloud ETL pipeline loading data into AWS Redshift data warehouse.",
    description: "Designed and implemented an ETL pipeline using Python to extract, transform, and load data into AWS Redshift data warehouse.",
    link: "#",
    thumbnail: "assets/thumbnails/cloud.svg",
    images: [],
    video: "",
    githubUrl: "",
    researchPdf: "",
    objective: "Build a scalable cloud data pipeline to ingest daily transactions into AWS Redshift.",
    requirements: "Python scripts utilizing Boto3 to upload files to S3 and execute Redshift COPY commands.",
    purpose: "Enable cloud-based analytics for high-volume enterprise data.",
    problem: "On-premises databases struggled with analytical query performance as data volumes grew.",
    approach: "Designed staging and target schemas in Redshift, automated S3 staging bucket uploads, and optimized COPY commands.",
    solution: "Automated cloud ETL pipeline powering Redshift analytical views.",
    result: "Accelerated complex analytical queries by 5x compared to legacy database.",
    technicalDetails: ["AWS Redshift", "AWS S3", "Python Boto3 SDK", "COPY command optimization"]
  }
];

// ──────────────────────────────────────────────
// Filter Categories
// ──────────────────────────────────────────────
const CATEGORIES = [
  "All",
  "Power BI",
  "Excel",
  "SQL",
  "Tableau",
  "Python",
  "Cloud/ETL",
  "App Dev",
  "Automation"
];

// ──────────────────────────────────────────────
// Experience Timeline
// ──────────────────────────────────────────────
const EXPERIENCE = [
  {
    role: "Executive Data Analyst & Customer Service Technical",
    company: "Innomotics India Ltd.",
    period: "Mar 2026 – Present",
    location: "Mumbai",
    highlights: [
      "Built Contract Intelligence Dashboard cutting lookup time from 5–10 min to ~10 seconds across 130+ contracts.",
      "Validated 75,670+ Installed Base records on global Master Data Governance initiative with Germany.",
      "Developed a QR-based asset management app (Flutter, Spring Boot, Docker, Kubernetes) for 16,218 drives."
    ],
    relatedProject: "installed-base-intelligence"
  },
  {
    role: "Data Analyst | Data Platform Developer",
    company: "Sounce Retail Pvt Ltd",
    period: "Feb 2025 – Mar 2026",
    location: "Mumbai",
    highlights: [
      "Automated Daily Run Rate via Excel VBA across 3,000+ SKUs — 90% processing time reduction.",
      "Built BI dashboards and Python ETL pipelines across 6 e-commerce marketplaces.",
      "Built a scraping bot cutting data collection from a full day to under an hour."
    ],
    relatedProject: "daily-run-rate-vba"
  },
  {
    role: "Data Analytics Intern",
    company: "Infotech",
    period: "Jul – Sep 2024",
    location: "Mumbai",
    highlights: [
      "Built AI automation workflows using Python, Scikit-learn, and OpenAI APIs."
    ],
    relatedProject: "resume-parser-bot"
  },
  {
    role: "Web Development Intern",
    company: "Unified Mentor Pvt Ltd",
    period: "Jan – Feb 2024",
    location: "Mumbai",
    highlights: [
      "Developed responsive web applications using React.js and REST APIs."
    ],
    relatedProject: null
  }
];

// ──────────────────────────────────────────────
// Certifications
// ──────────────────────────────────────────────
const CERTIFICATIONS = [
  {
    name: "Google Data Analytics Certificate",
    issuer: "Google",
    icon: "🎓",
    status: "Completed"
  },
  {
    name: "PL-300: Power BI Data Analyst",
    issuer: "Microsoft",
    icon: "📊",
    status: "In Progress"
  },
  {
    name: "Python for Data Science",
    issuer: "NPTEL",
    icon: "🐍",
    status: "Completed"
  },
  {
    name: "SQL for Data Science",
    issuer: "Coursera",
    icon: "🗃️",
    status: "Completed"
  }
];
