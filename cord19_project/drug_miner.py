"""
drug_miner.py - Extract drug/chemical mentions from CORD-19 abstracts
Builds drug-efficacy relationships and co-occurrence data
"""

import polars as pl
import re
from collections import defaultdict, Counter
from pathlib import Path
import pickle
from drug_dictionary import DRUG_EFFICACY_MAP, get_all_drugs, get_all_efficacies

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data/processed/cord19_compressed.parquet"
CACHE_FILE = BASE_DIR / "data/processed/drug_mentions_cache.pkl"

# Local File path used 
# DATA_FILE = Path("data/processed/cord19_compressed.parquet")
# CACHE_FILE = Path("data/processed/drug_mentions_cache.pkl")

# =============================================================================
# DRUG MENTION EXTRACTOR
# =============================================================================
class DrugMiner:
    """Extract and analyze drug mentions from CORD-19 abstracts."""
    
    def __init__(self, use_cache=True):
        self.drug_list = get_all_drugs()
        self.efficacy_list = get_all_efficacies()
        self.use_cache = use_cache
        
        # Data structures
        self.drug_counts = Counter()           # drug -> total mentions
        self.efficacy_counts = Counter()       # efficacy -> total mentions
        self.drug_papers = defaultdict(set)    # drug -> set of cord_uids
        self.drug_year_counts = defaultdict(Counter)  # drug -> {year: count}
        self.drug_month_counts = defaultdict(Counter) # drug -> {year_month: count}
        self.drug_cooccurrence = defaultdict(Counter) # drug -> {other_drug: count}
        self.efficacy_cooccurrence = defaultdict(Counter)
        self.papers_per_year = Counter()       # year -> paper count
        self.papers_per_month = Counter()      # year_month -> paper count
        
        # Build regex patterns for each drug (word boundaries)
        self.drug_patterns = {}
        for drug in self.drug_list:
            # Escape special chars and create pattern
            pattern = r'\b' + re.escape(drug) + r'\b'
            self.drug_patterns[drug] = re.compile(pattern, re.IGNORECASE)
    
    def find_drugs_in_text(self, text):
        """Find all drug mentions in a text."""
        if not text or text == "No Data":
            return set()
        
        found_drugs = set()
        text_lower = text.lower()
        
        for drug, pattern in self.drug_patterns.items():
            if pattern.search(text_lower):
                found_drugs.add(drug)
        
        return found_drugs
    
    def process_dataset(self, df):
        """Process entire dataset to extract drug mentions."""
        
        print("[INFO] Processing abstracts for drug mentions...")
        print(f"[INFO] Searching for {len(self.drug_list)} drugs")
        
        total = len(df)
        
        for i, row in enumerate(df.iter_rows(named=True)):
            # Progress update
            if (i + 1) % 50000 == 0:
                print(f"  Processed {i+1:,} / {total:,} papers...")
            
            abstract = row.get("abstract", "")
            cord_uid = row.get("cord_uid", "")
            publish_time = row.get("publish_time", "")
            
            # Extract year and month
            year = publish_time[:4] if len(publish_time) >= 4 else "Unknown"
            year_month = publish_time[:7] if len(publish_time) >= 7 else "Unknown"
            
            # Count papers per year/month
            if year.isdigit() and 2000 <= int(year) <= 2025:
                self.papers_per_year[year] += 1
                if len(year_month) == 7:
                    self.papers_per_month[year_month] += 1
            
            # Find drugs in abstract
            drugs_found = self.find_drugs_in_text(abstract)
            
            if not drugs_found:
                continue
            
            # Update counts
            for drug in drugs_found:
                self.drug_counts[drug] += 1
                self.drug_papers[drug].add(cord_uid)
                
                # Temporal counts
                if year.isdigit():
                    self.drug_year_counts[drug][year] += 1
                if len(year_month) == 7:
                    self.drug_month_counts[drug][year_month] += 1
                
                # Efficacy counts
                for efficacy in DRUG_EFFICACY_MAP.get(drug, []):
                    self.efficacy_counts[efficacy] += 1
            
            # Co-occurrence (drugs mentioned together in same abstract)
            drugs_list = list(drugs_found)
            for i, drug1 in enumerate(drugs_list):
                for drug2 in drugs_list[i+1:]:
                    self.drug_cooccurrence[drug1][drug2] += 1
                    self.drug_cooccurrence[drug2][drug1] += 1
                    
                    # Efficacy co-occurrence
                    for eff1 in DRUG_EFFICACY_MAP.get(drug1, []):
                        for eff2 in DRUG_EFFICACY_MAP.get(drug2, []):
                            if eff1 != eff2:
                                self.efficacy_cooccurrence[eff1][eff2] += 1
        
        print(f"[DONE] Processed {total:,} papers")
        print(f"[INFO] Found {len(self.drug_counts)} unique drugs mentioned")
    
    def save_cache(self):
        """Save processed data to cache file."""
        cache_data = {
            "drug_counts": dict(self.drug_counts),
            "efficacy_counts": dict(self.efficacy_counts),
            "drug_papers": {k: list(v) for k, v in self.drug_papers.items()},
            "drug_year_counts": {k: dict(v) for k, v in self.drug_year_counts.items()},
            "drug_month_counts": {k: dict(v) for k, v in self.drug_month_counts.items()},
            "drug_cooccurrence": {k: dict(v) for k, v in self.drug_cooccurrence.items()},
            "efficacy_cooccurrence": {k: dict(v) for k, v in self.efficacy_cooccurrence.items()},
            "papers_per_year": dict(self.papers_per_year),
            "papers_per_month": dict(self.papers_per_month),
        }
        
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump(cache_data, f)
        
        print(f"[SAVED] Cache to {CACHE_FILE}")
    
    def load_cache(self):
        """Load processed data from cache file."""
        if not CACHE_FILE.exists():
            return False
        
        print(f"[LOADING] Cache from {CACHE_FILE}")
        with open(CACHE_FILE, 'rb') as f:
            cache_data = pickle.load(f)
        
        self.drug_counts = Counter(cache_data["drug_counts"])
        self.efficacy_counts = Counter(cache_data["efficacy_counts"])
        self.drug_papers = {k: set(v) for k, v in cache_data["drug_papers"].items()}
        self.drug_year_counts = {k: Counter(v) for k, v in cache_data["drug_year_counts"].items()}
        self.drug_month_counts = {k: Counter(v) for k, v in cache_data["drug_month_counts"].items()}
        self.drug_cooccurrence = {k: Counter(v) for k, v in cache_data["drug_cooccurrence"].items()}
        self.efficacy_cooccurrence = {k: Counter(v) for k, v in cache_data["efficacy_cooccurrence"].items()}
        self.papers_per_year = Counter(cache_data["papers_per_year"])
        self.papers_per_month = Counter(cache_data["papers_per_month"])
        
        print("[LOADED] Cache successfully")
        return True
    
    # =========================================================================
    # QUERY METHODS (for dashboard)
    # =========================================================================
    
    def get_top_efficacies(self, n=15):
        """Get top N most mentioned efficacies."""
        return self.efficacy_counts.most_common(n)
    
    def get_top_drugs(self, n=15):
        """Get top N most mentioned drugs."""
        return self.drug_counts.most_common(n)
    
    def get_drugs_for_efficacy(self, efficacy, n=10):
        """Get top drugs for a given efficacy."""
        drugs = []
        for drug, effs in DRUG_EFFICACY_MAP.items():
            if efficacy.lower() in [e.lower() for e in effs]:
                count = self.drug_counts.get(drug, 0)
                if count > 0:
                    drugs.append((drug, count))
        
        return sorted(drugs, key=lambda x: x[1], reverse=True)[:n]
    
    def get_cooccurring_efficacies(self, selection, is_drug=True, n=10):
        """Get efficacies of drugs co-occurring with selection."""
        if is_drug:
            # Get drugs that co-occur with selected drug
            cooccur_drugs = self.drug_cooccurrence.get(selection.lower(), {})
            
            # Aggregate efficacies from co-occurring drugs
            eff_counts = Counter()
            for drug, count in cooccur_drugs.items():
                for eff in DRUG_EFFICACY_MAP.get(drug, []):
                    eff_counts[eff] += count
            
            return eff_counts.most_common(n)
        else:
            # Selection is an efficacy
            return self.efficacy_cooccurrence.get(selection.lower(), Counter()).most_common(n)
    
    def get_shared_efficacies(self, drug):
        """Get all efficacies for a drug (drugs with multiple labels)."""
        return DRUG_EFFICACY_MAP.get(drug.lower(), [])
    
    def get_drug_timeline(self, drug):
        """Get yearly % of papers mentioning drug (normalized)."""
        drug_years = self.drug_year_counts.get(drug.lower(), {})
        
        timeline = []
        for year in sorted(self.papers_per_year.keys()):
            total_papers = self.papers_per_year[year]
            drug_papers = drug_years.get(year, 0)
            pct = (drug_papers / total_papers * 100) if total_papers > 0 else 0
            timeline.append({
                "year": year,
                "papers": drug_papers,
                "total": total_papers,
                "percentage": round(pct, 3)
            })
        
        return timeline
    
    def get_monthly_change(self, drug):
        """Get month-over-month change in paper count for drug."""
        drug_months = self.drug_month_counts.get(drug.lower(), {})
        
        months_sorted = sorted(drug_months.keys())
        changes = []
        
        for i, month in enumerate(months_sorted):
            current = drug_months[month]
            previous = drug_months.get(months_sorted[i-1], 0) if i > 0 else 0
            change = current - previous
            pct_change = ((current - previous) / previous * 100) if previous > 0 else 0
            
            changes.append({
                "month": month,
                "count": current,
                "change": change,
                "pct_change": round(pct_change, 1)
            })
        
        return changes


# =============================================================================
# MAIN: Build cache if needed
# =============================================================================
def build_drug_cache(force_rebuild=False):
    """Build or load drug mention cache."""
    
    miner = DrugMiner()
    
    # Try to load cache
    if not force_rebuild and miner.load_cache():
        return miner
    
    # Build from scratch
    print("[INFO] Building drug mention cache (this takes ~5-10 minutes)...")
    
    df = pl.read_parquet(DATA_FILE)
    miner.process_dataset(df)
    miner.save_cache()
    
    return miner


if __name__ == "__main__":
    print("=" * 60)
    print("CORD-19 Drug Mining - Cache Builder")
    print("=" * 60)
    
    miner = build_drug_cache(force_rebuild=False)
    
    print("\n[SAMPLE RESULTS]")
    print("\nTop 10 Drugs:")
    for drug, count in miner.get_top_drugs(10):
        print(f"  {drug}: {count:,}")
    
    print("\nTop 10 Efficacies:")
    for eff, count in miner.get_top_efficacies(10):
        print(f"  {eff}: {count:,}")
