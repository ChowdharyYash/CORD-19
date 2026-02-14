# CORD-19 Research Paper Analysis Pipeline

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)](https://streamlit.io/)

A comprehensive data pipeline and interactive dashboard for analyzing the **COVID-19 Open Research Dataset (CORD-19)** — one of the largest collections of scientific papers on COVID-19 and related coronaviruses.

![Dashboard Preview](https://img.shields.io/badge/Papers%20Analyzed-970%2C000+-brightgreen)
![Drugs Tracked](https://img.shields.io/badge/Drugs%20Tracked-105-blue)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Part 1: Data Pipeline](#part-1-data-pipeline)
  - [Part 2: Exploratory Data Analysis](#part-2-exploratory-data-analysis)
  - [Part 3: Interactive Drug Dashboard](#part-3-interactive-drug-dashboard)
- [Dashboard Features](#dashboard-features)
- [Technical Details](#technical-details)
- [Sample Outputs](#sample-outputs)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

This project provides an end-to-end solution for:

1. **Extracting** ~1 million research papers from AWS S3 (CORD-19 dataset)
2. **Cleaning & Compressing** data into an optimized Parquet format (<800MB)
3. **Analyzing** publication trends, top journals, and research themes
4. **Mining** drug/chemical mentions across all abstracts
5. **Visualizing** insights through an interactive Streamlit dashboard

### Why This Project?

- **Hardware-Aware**: Designed for laptops with limited RAM (uses chunked processing)
- **No API Keys Required**: Uses unsigned S3 requests for public data access
- **Production-Ready**: Modular, well-documented, and extensible code
- **Interactive**: Real-time exploration of drug efficacies and trends

---

## Features

### Data Pipeline
- ✅ Stream download from AWS S3 (no credentials needed)
- ✅ Memory-safe chunked processing with Polars
- ✅ Robust date parsing for messy CORD-19 dates
- ✅ Zstandard compression (1.8GB → ~650MB)

### Exploratory Data Analysis
- ✅ Temporal analysis (papers per year/month)
- ✅ Top 10 journal identification
- ✅ Keyword frequency analysis (with scientific stopwords)
- ✅ Research trend tracking (Vaccine, Treatment, Epidemiology)
- ✅ Executive dashboard with 6 interactive charts

### Drug Analysis Dashboard
- ✅ 105 drugs with efficacy labels
- ✅ Drug co-occurrence analysis
- ✅ Chemical timeline (normalized by yearly publications)
- ✅ Month-over-month trend analysis
- ✅ Multi-efficacy drug exploration

---

## Project Structure

```
cord19_project/
│
├── 📁 Data Pipeline (Part 1)
│   ├── main.py                 # Entry point - runs full pipeline
│   ├── config.py               # Configuration constants
│   ├── downloader.py           # AWS S3 streaming module
│   ├── processor.py            # Data cleaning & compression
│   └── requirements.txt        # Dependencies
│
├── 📁 EDA Module (Part 2)
│   ├── eda_analysis.py         # Full EDA script (6 visualizations)
│   ├── eda_config.py           # EDA settings & stopwords
│   └── requirements_eda.txt    # Additional dependencies
│
├── 📁 Drug Dashboard (Part 3)
│   ├── dashboard.py            # Streamlit interactive UI
│   ├── drug_miner.py           # Text mining engine
│   ├── drug_dictionary.py      # 105 drugs + efficacy labels
│   ├── run_dashboard.py        # Dashboard launcher
│   └── requirements_dashboard.txt
│
├── 📁 data/
│   ├── raw/                    # Downloaded CSV (~1.8GB)
│   │   └── metadata.csv
│   └── processed/              # Compressed output
│       ├── cord19_compressed.parquet  # Main dataset (~650MB)
│       └── drug_mentions_cache.pkl    # Drug mining cache
│
├── 📁 outputs/
│   └── eda/                    # Generated HTML charts
│       ├── 01_papers_per_year.html
│       ├── 02_monthly_trend.html
│       ├── 03_top_journals.html
│       ├── 04_word_frequency.html
│       ├── 05_research_trends.html
│       └── 06_executive_dashboard.html
│
└── README.md                   # This file
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- 4GB+ RAM recommended
- 5GB free disk space
- Internet connection (for initial download)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/cord19-analysis.git
cd cord19-analysis
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install all dependencies at once
pip install polars boto3 pyarrow tqdm plotly streamlit pandas zstandard
```

Or use requirements files:

```bash
pip install -r requirements.txt
pip install -r requirements_eda.txt
pip install -r requirements_dashboard.txt
```

---

## Usage

### Part 1: Data Pipeline

Downloads and processes the CORD-19 dataset from AWS S3.

```bash
python main.py
```

**Expected Output:**
```
======================================================================
  CORD-19 DATA PIPELINE
======================================================================

[OK] All dependencies installed

======================================================================
STEP 1: DOWNLOAD FROM AWS S3
======================================================================
[DOWNLOAD] s3://ai2-semanticscholar-cord-19/latest/metadata.csv
[SIZE] 1800.0 MB
Progress: 100%|████████████████████| 1.80G/1.80G [05:30<00:00]
[SAVED] data\raw\metadata.csv

======================================================================
STEP 2: CLEAN AND COMPRESS
======================================================================
[INFO] Processing in chunks of 50,000 rows
   Chunk 1: 50,000 rows (Total: 50,000)
   Chunk 2: 50,000 rows (Total: 100,000)
   ...
[SAVED] data\processed\cord19_compressed.parquet
[SIZE] 650.0 MB
[SUCCESS] Under 800MB target!

======================================================================
[DONE] PIPELINE COMPLETE
======================================================================
Total time: 8m 30s
```

**Runtime:** 5-15 minutes (depending on internet speed)

---

### Part 2: Exploratory Data Analysis

Generates 6 interactive HTML visualizations.

```bash
python eda_analysis.py
```

**Expected Output:**
```
======================================================================
BLOCK 1: LOAD DATA & SUMMARY STATISTICS
======================================================================
[LOADED] data\processed\cord19_compressed.parquet
  Total Papers: 970,836
  Columns: ['cord_uid', 'title', 'abstract', 'publish_time', 'journal', 'url']

======================================================================
BLOCK 2: TEMPORAL ANALYSIS
======================================================================
[TEMPORAL KPIs]
  Peak Year: 2020 (350,000 papers)
  Peak Month: 2020-04 (45,000 papers)

[SAVED] outputs/eda/01_papers_per_year.html
[SAVED] outputs/eda/02_monthly_trend.html
...

======================================================================
EDA COMPLETE - SUMMARY
======================================================================
```

**Output Files:** Open any `.html` file in `outputs/eda/` in your browser.

**Runtime:** 2-4 minutes

---

### Part 3: Interactive Drug Dashboard

Launches a Streamlit web application for drug analysis.

```bash
python -m streamlit run dashboard.py
```

**First Run:** Builds drug mention cache (~5-10 minutes)  
**Subsequent Runs:** Loads from cache (~5 seconds)

**Access Dashboard:** Open `http://localhost:8501` in your browser

---

## Dashboard Features

| Feature | Description |
|---------|-------------|
| **Top Efficacies** | Most frequently mentioned drug efficacies (antiviral, anti-inflammatory, etc.) |
| **Top Chemicals for X** | Highest occurring drugs for selected efficacy |
| **Co-Occurring Efficacies** | Efficacies of drugs mentioned together with selected drug |
| **Shared Efficacies** | Multiple efficacy labels for a single drug |
| **Chemical Timeline** | Yearly % of papers mentioning drug (normalized) |
| **Monthly Change** | Month-over-month paper count changes |

### Tracked Drug Categories

- Antivirals (Remdesivir, Favipiravir, Molnupiravir)
- HIV Protease Inhibitors (Lopinavir, Ritonavir)
- Antimalarials (Hydroxychloroquine, Chloroquine)
- Corticosteroids (Dexamethasone, Prednisone)
- Monoclonal Antibodies (Tocilizumab, Bamlanivimab)
- Anticoagulants (Heparin, Enoxaparin)
- And 80+ more...

---

## Technical Details

### Libraries Used

| Library | Purpose |
|---------|---------|
| **Polars** | High-performance DataFrame operations |
| **Boto3** | AWS S3 access (unsigned requests) |
| **PyArrow** | Parquet file support |
| **Plotly** | Interactive visualizations |
| **Streamlit** | Web dashboard framework |
| **Zstandard** | Compression algorithm |

### Performance Optimizations

- **Chunked Processing:** 50,000 rows per batch to prevent memory overflow
- **Lazy Evaluation:** Polars defers computation until needed
- **Sampling:** Text mining uses 100K sample for speed
- **Caching:** Drug mentions stored in pickle for fast reloads
- **Parquet Format:** Columnar storage for efficient queries

### Data Schema

| Column | Type | Description |
|--------|------|-------------|
| `cord_uid` | String | Unique paper identifier |
| `title` | String | Paper title |
| `abstract` | String | Paper abstract |
| `publish_time` | String | Publication date (YYYY-MM-DD) |
| `journal` | String | Journal name |
| `url` | String | Link to paper |

---

## Sample Outputs

### Papers Per Year
Shows the explosion of COVID-19 research in 2020:

```
2019: ████ 45,000
2020: ████████████████████████████████████ 350,000
2021: ██████████████████████████████ 280,000
2022: ██████████████████████ 180,000
```

### Top Journals
```
1. bioRxiv: 85,000 papers (8.5%)
2. PLoS ONE: 42,000 papers (4.2%)
3. medRxiv: 38,000 papers (3.8%)
...
```

### Research Trends
```
Vaccine Research:     12.5% of papers
Treatment Research:   18.0% of papers
Epidemiology:          9.5% of papers
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `streamlit not recognized` | Use `python -m streamlit run dashboard.py` |
| `File not found: metadata.csv` | Run `python main.py` first |
| `UnicodeEncodeError` on Windows | Fixed in current version (no emojis) |
| `MemoryError` | Reduce `CHUNK_SIZE` in `config.py` to 25,000 |
| Dashboard shows blank | Wait 5 seconds, then refresh browser |
| Port 8501 in use | Run `python -m streamlit run dashboard.py --server.port 8502` |

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Dataset:** [CORD-19](https://github.com/allenai/cord19) by Allen Institute for AI
- **Data Source:** [AWS Open Data Registry](https://registry.opendata.aws/cord-19/)
- **Inspiration:** COVID-19 research community worldwide

---

## Citation

If you use this project in your research, please cite. 

---

<p align="center">
  Made with ❤️ for the research community
</p>
