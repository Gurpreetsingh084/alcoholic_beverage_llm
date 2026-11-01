# 🍾 AI Web Crawler for Alcoholic Beverage Data

[![Course](https://img.shields.io/badge/NZSE-BBIM713--Capstone--DA-blue.svg)](https://nzse.ac.nz)
[![Level](https://img.shields.io/badge/Level-7--Bachelor-darkgreen.svg)]()
[![Python](https://img.shields.io/badge/Python-3.11-yellow.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Completed--MVP-brightgreen.svg)]()
[![Automated Tests](https://img.shields.io/badge/Unit--Tests-15%2F15%20Passed-success.svg)]()
[![Ethics](https://img.shields.io/badge/Compliance-Aotearoa%20NZ%20Ethical%20Standards-purple.svg)]()

> **BBIM713 Capstone Project (Data Analytics) — Assessment 2 Portfolio**  
> *Bachelor of Business Information Management (Level 7)*  
> **Institution:** New Zealand Skills and Education College (NZSE), School of Tech  
> **Team:** Gurpreet Singh, Harsimran, Sukhbir  
> **Client (industry partner):** Dr Helena Bahrami | **Cohort:** BBIM7124C

---

## 📌 Executive Summary

Online alcoholic beverage retailing presents significant data fragmentation across heterogeneous e-commerce platforms. Traditional web scraping solutions rely heavily on brittle, hardcoded CSS/XPath selectors that break when website layouts change, failing to extract unstructured sensory tasting notes and contextual attributes.

This Capstone Project delivers an end-to-end **Minimum Viable Product (MVP)** combining an **Ethical Web Crawling Engine**, **Large Language Model (LLM) Semantic Extraction**, **Pydantic Validation & Entity Deduplication**, and **Relational Data Warehousing**. 

The system was evaluated across **18 configured retail and producer websites** (15 replayed from saved pages, 3 not crawled: 2 need a login, 1 is closed) in New Zealand and internationally, demonstrating superior extraction accuracy (**Macro F1-Score: 0.9349** vs. Rule Scraper: **0.4382**).

---

## 👥 Project Team & Work Allocation (LO1)

| Team Member | Student ID | Core Roles & Milestone Responsibilities | Codebase Modules |
| :--- | :---: | :--- | :--- |
| **Gurpreet Singh** | — | **Research & Risk Management:** research across the project; managed LLM hallucination risk (repeated prompt testing, checks against labelled ground truth) and duplicate-product risk (SequenceMatcher threshold 0.85). | Whole project (research, risk log, report writing) |
| **Harsimran** | — | **Planning & Coordination:** organised tasks and activities and coordinated the three team members. | Whole project (planning and coordination) |
| **Sukhbir** | — | **Technical Development:** requirements, extraction engine, database design (`beverages.db`), Pydantic validation, evaluation code comparing the LLM with the rule-based baseline. | `src/extraction/`, `src/validation/`, `database/`, `src/evaluation/`, `dashboard.py` |

---

## 📐 System Architecture Blueprint (9 Core Components)

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  SYSTEM SCHEMATIC ARCHITECTURE                                         │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
 [1. DATA SOURCES]                                                                                        
  └── 15 Active Commercial Retailer & Producer Websites (Liquorland NZ, Glengarry, Garage Project, etc.)   
                                      │                                                                  
                                      ▼                                                                  
 [2. DATA INGESTION & STORAGE]                                                                           
  ├── Ethical Crawler (Requests / Playwright)                                                            
  ├── Auto-Throttling (2.5s delay) + Academic User-Agent + robots.txt Parser                     
  └── Raw Storage: Local JSON/HTML dumps & SQLite staging table                                          
                                      │                                                                  
                                      ▼                                                                  
 [3. DATA PROCESSING & PREPROCESSING]                                                                    
  ├── HTML Sanitizer (BeautifulSoup4: Strips nav, footer, scripts, boilerplate)                          
  └── Non-Alcohol URL Blacklist Filter (/accessories/, /glassware/, /mixers/)                            
                                      │                                                                  
                                      ▼                                                                  
 [4 & 5. ML MODELS & AI EXTRACTION ENGINE]                                                               
  ├── Proposed AI Engine: LLM (GPT-4o mini) with Structured Pydantic JSON Prompting            
  │    └── Semantic Extraction: Extracts 10 Target Attributes (9 scored) + 'is_alcoholic_beverage' classification    
  └── Baseline Model (RQ2 Comparison): Traditional Rule-Based Scraper (Regex / CSS Selectors)            
                                      │                                                                  
                                      ▼                                                                  
 [DATA NORMALIZATION & ENTITY RESOLUTION]                                                                
  ├── Unit Normalizer (Volume -> standard 'ml'; Country -> canonical ISO name; Positive Prices)         
  └── Deduplication Engine (SequenceMatcher Token Similarity, Threshold: 0.85)                            
                                      │                                                                  
                  ┌───────────────────┴───────────────────┐                                              
                  ▼                                       ▼                                              
 [6. OUTPUT & VISUALIZATION]             [8. INTEGRATION & STORAGE]                                      
  ├── Single-Merchant Structured JSONs    ├── Relational Data Warehouse (SQLAlchemy/SQLite/Postgres)     
  ├── Master CSV Analytics Catalog        └── REST API / JSON Endpoints for ERP/BI integration (future work, not built)           
  └── Interactive Streamlit Web UI                                                                       
                                      │                                                                  
                                      ▼                                                                  
 [7. FEEDBACK LOOP & EVALUATION]                                                                         
  ├── 18-product Manually Labelled Ground Truth Benchmark (data/benchmark/ground_truth_sample.json)             
  ├── Automated Evaluation Engine (Precision, Recall, F1-Score for RQ2)                                  
  └── Catalog Inventory Metric Assertion Check (Scraped + Excluded == Total Website Baseline)            
                                      │                                                                  
                                      ▼                                                                  
 [9. SECURITY, ETHICS & COMPLIANCE]                                                                      
  ├── Ethical Crawling Compliance (robots.txt followed, 2.5s delay, zero PII collected)                    
  ├── Te Tiriti o Waitangi Alignment (Māori data sovereignty, ethical bicultural representation)         
  └── Post-Capstone Data Destruction & Handover Policy (Removal of data from student devices)            
```

---

## 🎯 Target Data Sources Directory

The system ingests product catalogs from **18 configured retailers and craft producers** (15 with saved sample pages, 3 not crawled: 2 need a login, 1 closed):

| Category | Merchant Name | Country | Domain Scope & Focus | Status |
| :--- | :--- | :---: | :--- | :---: |
| **NZ Retail Chains** | Liquorland NZ | NZ | National chain (Spirits, Wine, RTDs) | Active |
| **NZ Retail Chains** | Super Liquor NZ | NZ | Franchise chain (Beer cases, Spirits) | Active |
| **NZ Specialist** | Glengarry Wines | NZ | Fine wines, Single malts, Champagne | Active |
| **NZ Retail Supermarket** | Big Barrel NZ | NZ | Regional spirits, bulk beer, local wine | Active |
| **NZ Craft Specialist** | The Beer Cellar | NZ | Independent craft beer retailer | Active |
| **NZ Online Distributor**| Fine Wine Delivery Co | NZ | High-end boutique wine & rare spirits | Active |
| **NZ Retail Group** | Black Bull Liquor | NZ | Independent commercial liquor store | Active |
| **NZ Regional Chain** | Henry's Beer, Wine & Spirits | NZ | South Island regional beverage merchant | Closed (site closed) |
| **NZ Craft Producer** | Garage Project | NZ | Wellington craft brewery & natural wine | Active |
| **NZ Commercial Winery** | Villa Maria Estate | NZ | Marlborough & Hawke's Bay winery | Active |
| **NZ Craft Producer** | 8 Wired Brewing | NZ | Boutique barrel-aged brewery | Active |
| **NZ Craft Producer** | Epic Brewing Company | NZ | Craft IPA & Pale Ale manufacturer | Active |
| **Global Benchmark** | Dan Murphy's | Australia | Large-scale retail superstore | Active |
| **Global Benchmark** | The Whisky Exchange | UK | Global specialist spirits & single malts | Active |
| **Global Benchmark** | Master of Malt | UK | Boutique distilleries & craft spirits | Active |
| **Global Benchmark** | Total Wine & More | USA | US bourbons, international wines | Active |
| **Global Producer** | Cardhu Distillery | Scotland | Single malt scotch distillery | Exempt (Login) |
| **Global Benchmark** | First Choice Liquor | Australia | Commercial Australian liquor retailer | Exempt (Login) |

---

## 🧪 Empirical Evaluation & Key Findings

### 1. Research Question 2 (RQ2): LLM vs. Rule-Based Scraper Benchmark
Evaluated against an 18-item manually annotated ground truth dataset across the extracted attributes (10 extracted, 9 scored):

| Evaluation Metric | Traditional Rule-Based Scraper | Proposed LLM Semantic Extractor | Performance Delta |
| :--- | :---: | :---: | :---: |
| **Overall Precision** | `0.42` | **`0.91`** | **+0.49** |
| **Overall Recall** | `0.56` | **`0.99`** | **+0.43** |
| **Macro F1-Score** | `0.4382` | **`0.9349`** | **+0.4967 (+113.4%)** |

*Precision and recall are rounded to 2 decimals; `python main.py` prints all four decimals (report 8/11).*

*Insight:* While traditional rule scrapers broke when handling varying HTML selectors and missed unstructured tasting notes, the LLM (GPT-4o mini) achieved a **0.9349 Macro F1-Score**, accurately extracting nuanced sensory notes and standardizing heterogeneous attribute syntax. Macro F1 rose by 49.7 points (0.4382 to 0.9349), more than doubling.

**Field-level check (`field_accuracy.py`, micro-averaged):** 150 of 158 labelled values correct = **94.9%** (6 incorrect, 2 missing); precision 0.962, recall 0.949, F1 0.955. `main.py` reports macro-averaged scores and `field_accuracy.py` micro-averaged scores, so the two sets differ slightly. Counting the 3 shortened product names as correct gives 153 of 158 (96.8%). 11 of 18 products match on every field.


> **Limits:** the benchmark uses only 18 manually labelled products and 23 hand-prepared saved pages from 15 sites (a repeatable snapshot replay, not a live crawl), so the scores are indicative. The rule-based side is scored on 21 rows and the LLM side on 20 after merging 1 duplicate.
>
> SequenceMatcher (threshold 0.85) merged 1 cross-site duplicate in this run (Jameson Triple Distilled Irish Whiskey, Total Wine into Super Liquor), so 21 listings became 20 products. The catalogue count check (site total = scraped + excluded, test 12) is built, but real site totals have not been added yet, so it is shown as "not checked".

---

## 🧗 Obstacles We Hit and How We Beat Them

| Challenge | In simple words | What we did |
| :--- | :--- | :--- |
| LLM hallucination and errors | Hallucination: the AI states a value that is not on the page. | Structured Pydantic prompts, repeated prompt testing, checks against the 18-item ground truth. |
| Duplicate products | The same product appears on several sites with slightly different names. | Compared names with SequenceMatcher and tuned the match threshold to 0.85. |
| Sites needing a login | Some sites show products only to members or ask crawlers to stay out. | Left out Cardhu Distillery and First Choice Liquor (login); never bypassed access. Henrys NZ was left out because its website closed. |
| Small prototype data | 23 saved, hand-prepared sample pages from 15 sites and 18 labelled items. | Report scores as indicative; sample pages are easier than real shops, so next is a real-site crawl and a bigger labelled set. |

**What we learned:** prompts need iteration to curb hallucination, thresholds need balance, and governance matters beyond code.

---

## 🏁 Conclusion: Answers to the Research Questions

| Research Question | Answer | Evidence |
| :--- | :---: | :--- |
| **RQ1: Crawling** | Partly | One pipeline ran on saved sample pages from 15 sites without per-site rules (23 pages gave 21 valid listings). A live crawl is still untested. |
| **RQ2: Extraction accuracy** | Yes | Macro F1 0.93 vs 0.44; structured prompts and validation keep results consistent. Only 18 labelled items, so the scores are indicative. |
| **RQ3: Dataset quality** | Yes | 21 listings became 20 products; 15 of 15 tests passed because every stage is checked. |

**Recommendation**
* Use AI to read product pages instead of writing rules for each site.
* Let a person check doubtful records to catch AI mistakes.

**Next steps**
* Crawl full catalogues and check totals per site.
* Build a bigger labelled test set.

**In one sentence:** an AI crawler can turn messy shop pages into one clean, trusted catalogue when it crawls politely and every result is checked.

---

## 🖥️ Interactive Web Dashboard UI (Proposal Milestone 1.2.3)

The project includes an interactive **Streamlit Visual Analytics Dashboard (`dashboard.py`)** featuring:
1. **Executive KPI Metric Cards:** Counts of canonical items, dropped accessories, average price, strength, and F1-scores. Current values: 20 canonical products, 2 excluded accessories, LLM macro F1 0.9349 (+49.7 points on the rule-based 0.4382). Average price and average ABV are recalculated from the catalogue on every run.
2. **Dynamic Search & Slider Filters:** Filter by category, country of origin, and price boundaries.
3. **Visual Analytics Charts:**
   * Alcohol Content ($\text{ABV}\%$) vs. Retail Price ($\$\text{NZD}$) Scatter Plot.
   * Cross-Merchant Average Price Comparison Bar Chart.
   * Empirical Model Performance Comparison (Rule Scraper vs. LLM Extractor).
4. **Data source banner:** the dashboard states that data is a replay of saved retailer pages (a repeatable benchmark snapshot), not a live crawl.
5. **Caveats:** prices mix currencies that were not converted, so the average price and the cross-merchant comparison are indicative only. The Lagavulin listing (144.02, a UK price) is the highest price in the catalogue. The dashboard labels prices "$ NZD" although AU, UK and US prices are not converted.

---

## 🛡️ Ethical Governance & Te Tiriti o Waitangi Compliance (LO5 / GPO 03)

1. **Ethical Crawling Standards:** The crawler follows each site's `robots.txt` rules using `urllib.robotparser` (covered by tests 01 to 03), waits $2.5\text{s}$ between requests and identifies as an academic research crawler via a custom `User-Agent`. The demo replays saved sample pages; a live full-site crawl has not been run yet. Two sites that need a login (Cardhu Distillery, First Choice Liquor) were left out and never bypassed; Henrys NZ was left out because its website closed.
2. **Public-Domain Scope & Data Privacy:** The system strictly collects public product metadata (name, price, volume, tasting notes). **No personally identifiable information (PII), customer logins, or payment data are collected or stored.**
3. **Te Tiriti o Waitangi Alignment:** Respects Māori Data Sovereignty by ensuring transparency in data processing, maintaining ethical stewardship, and preventing cultural misrepresentation in regional beverage classification.
4. **Data Destruction & Handover Policy:** In accordance with institutional research ethics, all temporary local caches and raw scrape files will be purged from student hardware upon final assessment grading, with all master artifacts handed over to NZSE academic supervisors.

---

## ✅ Automated Test Suite Verification (15/15 Passed)

The system features an automated unit test suite (`tests/test_suite.py`) testing all architectural layers. A further 7 integrity tests (`tests/test_integrity.py`) check that no values are invented:

```text
====================================================================================================
BBIM713 CAPSTONE PROJECT: AUTOMATED SYSTEM TEST SUITE
====================================================================================================
  01. test_01_user_agent_configuration              [Crawler & Ethical Compliance]       ✓ PASS
  02. test_02_rate_limit_parameters                 [Crawler & Ethical Compliance]       ✓ PASS
  03. test_03_robots_checker_initialization         [Crawler & Ethical Compliance]       ✓ PASS
  04. test_04_html_boilerplate_stripping            [Preprocessing & Sanitization]       ✓ PASS
  05. test_05_non_alcoholic_url_blacklisting        [Preprocessing & Sanitization]       ✓ PASS
  06. test_06_rule_based_extractor                  [Extraction Engine]                  ✓ PASS
  07. test_07_llm_semantic_extractor_schema         [Extraction Engine]                  ✓ PASS
  08. test_08_volume_normalization                  [Normalization & Validation]         ✓ PASS
  09. test_09_country_normalization                 [Normalization & Validation]         ✓ PASS
  10. test_10_pydantic_boundary_validation          [Normalization & Validation]         ✓ PASS
  11. test_11_entity_deduplication                  [Deduplication & Assertions]         ✓ PASS
  12. test_12_catalog_inventory_assertion_equation  [Deduplication & Assertions]         ✓ PASS
  13. test_13_database_crud_persistence             [Database & Persistence]             ✓ PASS
  14. test_14_metrics_calculator_precision_recall_f1[Evaluation Metrics]                 ✓ PASS
  15. test_15_target_merchants_config_coverage      [Data Sources & Config]              ✓ PASS
----------------------------------------------------------------------------------------------------
OVERALL STATISTICS: 15 Executed | 15 Passed | 0 Failed | Pass Rate: 100.00% (Time: 4.47s)
====================================================================================================
```

---

## 🚀 Quickstart & Replication Guide

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/Gurpreetsingh084/alcoholic_beverage_llm.git
cd alcoholic_beverage_llm
pip install -r requirements.txt
```

### 2. Configure Environment Variables
```bash
cp .env.example .env
```

### 3. Run the End-to-End Pipeline
```bash
python main.py
```

### 4. Launch Interactive Web Dashboard
```bash
python -m streamlit run dashboard.py
```

### 5. Execute Automated Test Suite
```bash
python tests/test_suite.py
python tests/test_integrity.py
```

### 6. Field-Level Accuracy Report (no OpenAI calls)
```bash
python field_accuracy.py
```

---

## 📁 Repository Directory Structure

```text
alcoholic_beverage_llm/
│
├── config/
│   ├── settings.py                     # Crawler limits, delays, database connection
│   ├── sites_config.yaml               # 18 Target NZ & Global merchant configurations
│   └── schema.json                     # JSON Schema definition for beverage attributes
│
├── data/
│   ├── raw/                            # Intermediate HTML and raw scraped payloads
│   ├── processed/                      # Output single-merchant JSONs & master CSV
│   │   ├── master_beverage_catalog.csv
│   │   ├── master_beverage_catalog.json
│   │   └── pipeline_metrics.json
│   └── benchmark/                      # Ground truth test dataset
│       └── ground_truth_sample.json
│
├── database/
│   ├── schema.sql                      # Products table DDL for SQLite
│   ├── db_connection.py                # SQLAlchemy engine & session factory
│   └── crud.py                         # CRUD operations for products & merchants
│
├── src/
│   ├── export_merchants.py             # One JSON file per merchant (15 files)
│   ├── crawler/
│   │   ├── robots_checker.py           # Robots.txt validation & auto-throttling
│   │   ├── static_scraper.py           # Requests polite crawler
│   │   └── dynamic_scraper.py          # Playwright dynamic DOM renderer
│   ├── preprocessing/
│   │   ├── html_cleaner.py             # BeautifulSoup boilerplate stripper
│   │   └── url_filter.py               # Non-alcohol URL & keyword blacklisting
│   ├── extraction/
│   │   ├── base_extractor.py           # Abstract base extractor interface
│   │   ├── rule_based_extractor.py     # Traditional regex/selector baseline
│   │   ├── llm_extractor.py            # LLM semantic parser (GPT-4o mini)
│   │   └── prompt_templates.py         # System & user extraction prompt schemas
│   ├── validation/
│   │   ├── models.py                   # Pydantic schema enforcing the product fields
│   │   ├── normalizer.py               # Volume (mL) & ISO country normalizer
│   │   └── deduplicator.py             # SequenceMatcher entity resolution
│   └── evaluation/
│       └── metrics_calculator.py       # Precision, Recall & Macro F1 calculator
│
├── tests/
│   ├── test_suite.py                   # 15 Automated System Unit Tests
│   └── test_integrity.py               # 7 integrity tests (no invented values)
│
├── dashboard.py                        # Streamlit Visual Analytics Web Application
├── main.py                             # Master CLI pipeline execution script
├── PORTFOLIO.md                        # Portfolio documentation & showcase page
├── RUN_ME.txt                          # Step-by-step run guide (Windows, Python 3.11)
├── field_accuracy.py                   # Field-level accuracy report vs answer key (reads saved output only)
├── list_products.py                    # Lists DB products by name; writes products_20.csv (pre-fuzzy-merge list)
├── summary_db.py / inspect_db.py / check_db.py  # Quick SQLite inspection helpers
├── rebuild_db.py                       # Re-saves merchant JSONs into SQLite (no OpenAI calls)
├── show_db.py                          # Prints the SQLite table for screenshots
├── requirements.txt                    # Project Python dependencies
└── README.md                           # Main GitHub repository landing page
```