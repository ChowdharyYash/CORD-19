"""
run_dashboard.py - Setup and Launch CORD-19 Drug Dashboard
==========================================================
This script:
1. Checks dependencies
2. Builds the drug mention cache (first run only, ~5-10 min)
3. Launches the Streamlit dashboard

Run with: python run_dashboard.py
"""

import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed."""
    required = ["streamlit", "polars", "plotly", "pandas"]
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print("[ERROR] Missing packages:", ", ".join(missing))
        print("\nInstall with:")
        print("  pip install -r requirements_dashboard.txt")
        return False
    
    print("[OK] All dependencies installed")
    return True


def check_data_file():
    """Check if parquet file exists."""
    data_file = Path("data/processed/cord19_compressed.parquet")
    
    if not data_file.exists():
        print(f"[ERROR] Data file not found: {data_file}")
        print("\nPlease run the data pipeline first:")
        print("  python main.py")
        return False
    
    size_mb = data_file.stat().st_size / (1024**2)
    print(f"[OK] Data file found: {data_file} ({size_mb:.0f} MB)")
    return True


def build_cache_if_needed():
    """Build drug mention cache if not exists."""
    cache_file = Path("data/processed/drug_mentions_cache.pkl")
    
    if cache_file.exists():
        size_mb = cache_file.stat().st_size / (1024**2)
        print(f"[OK] Cache file found: {cache_file} ({size_mb:.1f} MB)")
        return True
    
    print("\n" + "=" * 60)
    print("FIRST RUN: Building drug mention cache")
    print("This takes ~5-10 minutes (one-time only)")
    print("=" * 60 + "\n")
    
    # Import and run miner
    from drug_miner import build_drug_cache
    miner = build_drug_cache(force_rebuild=False)
    
    print("\n[OK] Cache built successfully!")
    return True


def launch_dashboard():
    """Launch Streamlit dashboard."""
    print("\n" + "=" * 60)
    print("LAUNCHING DASHBOARD")
    print("=" * 60)
    print("\nDashboard will open in your browser...")
    print("Press Ctrl+C to stop the server\n")
    
    # Launch streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])


def main():
    print("=" * 60)
    print("CORD-19 Drug Analysis Dashboard")
    print("=" * 60 + "\n")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Step 2: Check data file
    if not check_data_file():
        sys.exit(1)
    
    # Step 3: Build cache if needed
    if not build_cache_if_needed():
        sys.exit(1)
    
    # Step 4: Launch dashboard
    launch_dashboard()


if __name__ == "__main__":
    main()
