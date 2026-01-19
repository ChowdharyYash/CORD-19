"""
processor.py - Clean and Compress CORD-19 Data
Uses Polars for memory-safe processing on laptops
"""

import polars as pl
from pathlib import Path
from datetime import datetime
import config

# =============================================================================
# DATE PARSER (Handles CORD-19's Messy Dates)
# =============================================================================
def parse_publish_time(date_str: str) -> str:
    """
    Parse various date formats found in CORD-19 dataset.
    Returns ISO format (YYYY-MM-DD) or 'Unknown' if unparseable.
    """
    if date_str is None or str(date_str).strip() == "":
        return "Unknown"
    
    date_str = str(date_str).strip()
    
    for fmt in config.DATE_FORMATS:
        try:
            parsed = datetime.strptime(date_str, fmt)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue
    
    # Handle year only
    if len(date_str) == 4 and date_str.isdigit():
        return f"{date_str}-01-01"
    
    # Handle year-month
    if len(date_str) == 7 and "-" in date_str:
        try:
            year, month = date_str.split("-")
            if year.isdigit() and month.isdigit():
                return f"{year}-{month.zfill(2)}-01"
        except:
            pass
    
    return "Unknown"


# =============================================================================
# SCHEMA DEFINITION
# =============================================================================
def get_schema() -> dict:
    """Define explicit schema for CSV parsing."""
    return {
        "cord_uid": pl.Utf8,
        "sha": pl.Utf8,
        "source_x": pl.Utf8,
        "title": pl.Utf8,
        "doi": pl.Utf8,
        "pmcid": pl.Utf8,
        "pubmed_id": pl.Utf8,
        "license": pl.Utf8,
        "abstract": pl.Utf8,
        "publish_time": pl.Utf8,
        "authors": pl.Utf8,
        "journal": pl.Utf8,
        "mag_id": pl.Utf8,
        "who_covidence_id": pl.Utf8,
        "arxiv_id": pl.Utf8,
        "pdf_json_files": pl.Utf8,
        "pmc_json_files": pl.Utf8,
        "url": pl.Utf8,
        "s2_id": pl.Utf8,
    }


# =============================================================================
# DATE PROCESSING
# =============================================================================
def process_dates_chunked(df: pl.DataFrame) -> pl.DataFrame:
    """Process dates using map_elements."""
    print("[INFO] Parsing dates...")
    
    return df.with_columns(
        pl.col("publish_time")
        .map_elements(parse_publish_time, return_dtype=pl.Utf8)
        .alias("publish_time")
    )


# =============================================================================
# CHUNKED PROCESSING
# =============================================================================
def process_in_chunks(
    input_path: Path,
    output_path: Path,
    chunk_size: int = config.CHUNK_SIZE
) -> pl.DataFrame:
    """Process large CSV in chunks to prevent memory overflow."""
    
    print(f"[INFO] Processing in chunks of {chunk_size:,} rows")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    reader = pl.read_csv_batched(
        input_path,
        dtypes=get_schema(),
        batch_size=chunk_size,
        ignore_errors=True,
        truncate_ragged_lines=True,
        encoding="utf8-lossy",
    )
    
    all_chunks = []
    chunk_num = 0
    total_rows = 0
    
    print("[INFO] Processing chunks:")
    
    while True:
        batches = reader.next_batches(1)
        if not batches:
            break
        
        df_chunk = batches[0]
        chunk_num += 1
        
        # Select essential columns
        available_cols = [c for c in config.KEEP_COLUMNS if c in df_chunk.columns]
        df_chunk = df_chunk.select(available_cols)
        
        # Fill missing values
        df_chunk = df_chunk.with_columns([
            pl.col("title").fill_null(config.FILL_VALUE),
            pl.col("abstract").fill_null(config.FILL_VALUE),
            pl.col("journal").fill_null("Unknown Journal"),
            pl.col("url").fill_null(""),
            pl.col("publish_time").fill_null("Unknown"),
        ])
        
        # Process dates
        df_chunk = process_dates_chunked(df_chunk)
        
        # Strip whitespace
        df_chunk = df_chunk.with_columns([
            pl.col("title").str.strip_chars(),
            pl.col("abstract").str.strip_chars(),
        ])
        
        rows_in_chunk = len(df_chunk)
        total_rows += rows_in_chunk
        print(f"   Chunk {chunk_num}: {rows_in_chunk:,} rows (Total: {total_rows:,})")
        
        all_chunks.append(df_chunk)
    
    # Combine chunks
    print(f"\n[INFO] Combining {len(all_chunks)} chunks...")
    df_final = pl.concat(all_chunks)
    
    # Remove duplicates
    print("[INFO] Removing duplicates...")
    before_dedup = len(df_final)
    df_final = df_final.unique(subset=["cord_uid"], keep="first")
    after_dedup = len(df_final)
    print(f"   Removed {before_dedup - after_dedup:,} duplicates")
    
    return df_final


# =============================================================================
# SAVE COMPRESSED PARQUET
# =============================================================================
def save_compressed_parquet(
    df: pl.DataFrame,
    output_path: Path,
    compression_level: int = config.COMPRESSION_LEVEL
) -> Path:
    """Save DataFrame as Zstandard-compressed Parquet."""
    
    print(f"\n[INFO] Saving compressed Parquet...")
    print(f"   Compression: Zstandard (level {compression_level})")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df.write_parquet(
        output_path,
        compression="zstd",
        compression_level=compression_level,
        use_pyarrow=True,
    )
    
    size_mb = output_path.stat().st_size / (1024**2)
    print(f"[SAVED] {output_path}")
    print(f"[SIZE] {size_mb:.1f} MB")
    
    if size_mb < 800:
        print("[SUCCESS] Under 800MB target!")
    else:
        print("[NOTE] File exceeds 800MB target")
    
    return output_path


# =============================================================================
# MAIN PROCESSING FUNCTION
# =============================================================================
def process_cord19(input_path: Path = None, output_path: Path = None) -> Path:
    """Complete processing pipeline."""
    
    input_path = input_path or config.RAW_FILE
    output_path = output_path or config.OUTPUT_FILE
    
    print("=" * 60)
    print("CORD-19 Data Processor")
    print("=" * 60)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    input_size_mb = input_path.stat().st_size / (1024**2)
    print(f"[INPUT] {input_path} ({input_size_mb:.1f} MB)")
    
    df = process_in_chunks(input_path, output_path)
    
    print(f"\n[STATS] Final Statistics:")
    print(f"   Total rows: {len(df):,}")
    print(f"   Columns: {df.columns}")
    
    return save_compressed_parquet(df, output_path)


if __name__ == "__main__":
    process_cord19()
