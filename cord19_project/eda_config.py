"""
eda_config.py - Configuration for CORD-19 Exploratory Data Analysis
Contains KPI definitions, stopwords, and research trend keywords
"""

from pathlib import Path

# =============================================================================
# FILE PATHS
# =============================================================================
DATA_FILE = Path("data/processed/cord19_compressed.parquet")
OUTPUT_DIR = Path("outputs/eda")

# =============================================================================
# SAMPLING SETTINGS (Hardware-Aware)
# =============================================================================
# For text mining on 1M+ abstracts, we sample to keep laptop responsive
TEXT_SAMPLE_SIZE = 100_000  # Sample for word frequency analysis
VIZ_SAMPLE_SIZE = 50_000    # Sample for heavy visualizations

# =============================================================================
# STOPWORDS (Extended list for scientific papers)
# =============================================================================
STOPWORDS = {
    # Standard English stopwords
    'a', 'an', 'the', 'and', 'or', 'but', 'if', 'then', 'else', 'when',
    'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
    'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
    'further', 'once', 'here', 'there', 'where', 'why', 'how', 'all',
    'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
    'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can',
    'will', 'just', 'should', 'now', 'also', 'as', 'is', 'are', 'was',
    'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
    'does', 'did', 'doing', 'would', 'could', 'ought', 'of', 'it', 'its',
    'this', 'that', 'these', 'those', 'am', 'he', 'she', 'they', 'we',
    'you', 'i', 'me', 'my', 'your', 'his', 'her', 'our', 'their', 'what',
    'which', 'who', 'whom', 'while', 'both', 'either', 'neither', 'because',
    
    # Scientific/academic stopwords
    'study', 'studies', 'result', 'results', 'method', 'methods', 'using',
    'used', 'use', 'based', 'however', 'may', 'might', 'et', 'al', 'fig',
    'figure', 'table', 'data', 'analysis', 'found', 'showed', 'shown',
    'show', 'shows', 'including', 'included', 'include', 'associated',
    'significantly', 'significant', 'compared', 'although', 'thus',
    'therefore', 'conclusion', 'conclusions', 'background', 'objective',
    'objectives', 'aim', 'aims', 'introduction', 'discussion', 'abstract',
    'paper', 'article', 'research', 'researchers', 'investigated',
    'examined', 'observed', 'reported', 'demonstrated', 'suggested',
    'indicate', 'indicates', 'indicated', 'conclusion', 'conclusions',
    'one', 'two', 'three', 'first', 'second', 'new', 'well', 'within',
    
    # CORD-19 specific noise
    'covid', 'coronavirus', 'sars', 'cov', 'ncov', 'pandemic', 'outbreak',
    'disease', 'diseases', 'infection', 'infections', 'infected', 'virus',
    'viral', 'patient', 'patients', 'case', 'cases', 'health', 'medical',
    'clinical', 'hospital', 'no', 'data',  # "No Data" fill value
}

# =============================================================================
# RESEARCH TREND KEYWORDS (For KPI Tracking)
# =============================================================================
RESEARCH_TRENDS = {
    "Vaccine Research": [
        'vaccine', 'vaccines', 'vaccination', 'vaccinated', 'immunization',
        'immunize', 'mrna', 'antibody', 'antibodies', 'immunogenicity',
        'booster', 'dose', 'efficacy'
    ],
    "Treatment & Therapeutics": [
        'treatment', 'treatments', 'therapy', 'therapies', 'therapeutic',
        'drug', 'drugs', 'medication', 'antiviral', 'remdesivir',
        'hydroxychloroquine', 'dexamethasone', 'monoclonal', 'plasma'
    ],
    "Epidemiology & Transmission": [
        'transmission', 'spread', 'spreading', 'epidemiology', 'epidemic',
        'reproduction', 'r0', 'contact', 'tracing', 'quarantine',
        'isolation', 'lockdown', 'social', 'distancing', 'incubation'
    ],
}

# =============================================================================
# KPI DEFINITIONS (Business Intelligence)
# =============================================================================
"""
KPI LOGIC EXPLANATION:

1. TEMPORAL KPIs:
   - Total Papers: Count of unique cord_uid
   - Monthly Publication Rate: Papers per month (trend indicator)
   - Peak Month: Month with highest publication volume
   - Year-over-Year Growth: % change in annual publications

2. JOURNAL KPIs:
   - Top Journal Share: % of papers from top journal
   - Top 10 Concentration: % of papers from top 10 journals
   - Journal Diversity Index: Unique journals / total papers

3. RESEARCH TREND KPIs:
   - Vaccine Research %: Papers mentioning vaccine keywords / total
   - Treatment Research %: Papers mentioning treatment keywords / total  
   - Epidemiology Research %: Papers mentioning transmission keywords / total
   - Trend Growth Rate: Month-over-month change in each trend

These KPIs help answer:
- "How fast is COVID research growing?"
- "Which journals dominate the field?"
- "Is vaccine research increasing over time?"
"""

# =============================================================================
# VISUALIZATION SETTINGS
# =============================================================================
PLOTLY_TEMPLATE = "plotly_white"
COLOR_PALETTE = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]
