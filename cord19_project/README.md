# CORD-19 Data Pipeline - Setup Guide

## 🚀 Quick Start for First-Time VS Code Users

### Step 1: Open VS Code Terminal
- Press `Ctrl + `` (backtick) or go to View → Terminal

### Step 2: Create Project Folder
```bash
mkdir cord19_project
cd cord19_project
```

### Step 3: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install polars boto3 zstandard pyarrow tqdm
```

### Step 5: Create the Python Files
- Copy `config.py`, `downloader.py`, `processor.py`, and `main.py` into your project folder

### Step 6: Run the Pipeline
```bash
python main.py
```

## 📁 Project Structure
```
cord19_project/
├── config.py        # Configuration constants
├── downloader.py    # S3 streaming module
├── processor.py     # Data cleaning & compression
├── main.py          # Entry point
├── data/
│   ├── raw/         # Downloaded CSV (auto-created)
│   └── processed/   # Final Parquet file (auto-created)
```

## ⚠️ Hardware Notes
- RAM: Minimum 4GB free recommended
- Disk: ~3GB free space needed during processing
- Time: ~5-15 minutes depending on internet speed

## 📊 Expected Output
- Final file: `data/processed/cord19_compressed.parquet`
- Target size: Under 800MB (Zstandard compressed)
