"""
main.py - CORD-19 Pipeline Entry Point
Run this file to download and process the dataset
"""

import sys
import time
from pathlib import Path

# =============================================================================
# DEPENDENCY CHECK
# =============================================================================
def check_dependencies():
    """Verify all required packages are installed."""
    required = {
        "polars": "polars",
        "boto3": "boto3", 
        "tqdm": "tqdm",
        "pyarrow": "pyarrow",
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("[ERROR] Missing dependencies. Run:")
        print(f"   pip install {' '.join(missing)}")
        sys.exit(1)
    
    print("[OK] All dependencies installed")


# =============================================================================
# MAIN PIPELINE
# =============================================================================
def main():
    """
    Execute the complete CORD-19 pipeline:
    1. Download from AWS S3
    2. Clean and compress
    """
    print("=" * 70)
    print("  CORD-19 DATA PIPELINE")
    print("  Extraction & Compression Module")
    print("=" * 70)
    print()
    
    check_dependencies()
    print()
    
    import config
    from downloader import download_cord19_metadata
    from processor import process_cord19
    
    start_time = time.time()
    
    # STEP 1: Download
    print("=" * 70)
    print("STEP 1: DOWNLOAD FROM AWS S3")
    print("=" * 70)
    
    try:
        raw_file = download_cord19_metadata(force_download=False)
        print()
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        print("\nTroubleshooting:")
        print("   1. Check internet connection")
        print("   2. Ensure boto3 is installed: pip install boto3")
        sys.exit(1)
    
    # STEP 2: Process
    print("=" * 70)
    print("STEP 2: CLEAN AND COMPRESS")
    print("=" * 70)
    
    try:
        output_file = process_cord19()
        print()
    except Exception as e:
        print(f"[ERROR] Processing failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # SUMMARY
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    
    print("=" * 70)
    print("[DONE] PIPELINE COMPLETE")
    print("=" * 70)
    print(f"Output file: {output_file}")
    print(f"File size: {output_file.stat().st_size / (1024**2):.1f} MB")
    print(f"Total time: {minutes}m {seconds}s")
    print()


if __name__ == "__main__":
    main()
