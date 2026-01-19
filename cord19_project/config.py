"""
config.py - Configuration constants for CORD-19 pipeline
"""

from pathlib import Path

# =============================================================================
# AWS S3 CONFIGURATION (Unsigned/Public Access)
# =============================================================================
S3_BUCKET = "ai2-semanticscholar-cord-19"
S3_KEY = "latest/metadata.csv"
S3_REGION = "us-west-2"

# =============================================================================
# LOCAL PATHS
# =============================================================================
BASE_DIR = Path("data")
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"

RAW_FILE = RAW_DIR / "metadata.csv"
OUTPUT_FILE = PROCESSED_DIR / "cord19_compressed.parquet"

# =============================================================================
# SCHEMA: Columns to Keep
# =============================================================================
KEEP_COLUMNS = [
    "cord_uid",
    "title",
    "abstract",
    "publish_time",
    "journal",
    "url",
]

# =============================================================================
# PROCESSING SETTINGS
# =============================================================================
CHUNK_SIZE = 50_000
FILL_VALUE = "No Data"
COMPRESSION_LEVEL = 9

# =============================================================================
# DATE PARSING FORMATS
# =============================================================================
DATE_FORMATS = [
    "%Y-%m-%d",
    "%Y-%m",
    "%Y",
    "%d-%m-%Y",
    "%m/%d/%Y",
]
