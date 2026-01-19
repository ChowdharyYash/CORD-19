"""
eda_analysis.py - CORD-19 Exploratory Data Analysis
==================================================
Modular analysis blocks for VS Code execution.

Run each block separately or run the entire script.
Hardware-aware: uses sampling for heavy operations.

BLOCKS:
  1. Load Data & Summary Statistics
  2. Temporal Analysis (Papers per Month/Year)
  3. Journal Analysis (Top 10 Journals)
  4. Text Mining (Word Frequency)
  5. Research Trend KPIs
  6. Executive Dashboard
"""

import polars as pl
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter
import re
from pathlib import Path
import eda_config as cfg

# Create output directory
cfg.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# BLOCK 1: LOAD DATA & SUMMARY STATISTICS
# =============================================================================
print("=" * 70)
print("BLOCK 1: LOAD DATA & SUMMARY STATISTICS")
print("=" * 70)

# Load parquet (fast - columnar format)
df = pl.read_parquet(cfg.DATA_FILE)

# Basic stats
total_papers = len(df)
total_columns = len(df.columns)
memory_mb = df.estimated_size("mb")

print(f"\n[LOADED] {cfg.DATA_FILE}")
print(f"  Total Papers: {total_papers:,}")
print(f"  Columns: {df.columns}")
print(f"  Memory Usage: {memory_mb:.1f} MB")

# Missing value analysis
print("\n[MISSING VALUES]")
for col in df.columns:
    null_count = df[col].null_count()
    null_pct = (null_count / total_papers) * 100
    print(f"  {col}: {null_count:,} ({null_pct:.1f}%)")

# "No Data" counts (our fill value)
no_data_title = df.filter(pl.col("title") == "No Data").height
no_data_abstract = df.filter(pl.col("abstract") == "No Data").height
print(f"\n[FILL VALUES]")
print(f"  Titles with 'No Data': {no_data_title:,}")
print(f"  Abstracts with 'No Data': {no_data_abstract:,}")

# =============================================================================
# BLOCK 2: TEMPORAL ANALYSIS
# =============================================================================
print("\n" + "=" * 70)
print("BLOCK 2: TEMPORAL ANALYSIS")
print("=" * 70)

# Parse dates and extract year/month
df_temporal = df.with_columns([
    pl.col("publish_time").str.slice(0, 4).alias("year"),
    pl.col("publish_time").str.slice(0, 7).alias("year_month"),
])

# Filter valid years (exclude "Unknown" and unrealistic dates)
# Step 1: Keep only rows where year is exactly 4 digits
df_temporal = df_temporal.filter(
    pl.col("year").str.contains(r"^\d{4}$")
)

# Step 2: Now safe to cast and filter by range
df_temporal = df_temporal.filter(
    (pl.col("year").cast(pl.Int32) >= 2000) &
    (pl.col("year").cast(pl.Int32) <= 2025)
)

# Papers per year
papers_by_year = (
    df_temporal
    .group_by("year")
    .agg(pl.count().alias("paper_count"))
    .sort("year")
).to_pandas()

# Papers per month (for detailed trend)
papers_by_month = (
    df_temporal
    .filter(pl.col("year_month").str.len_chars() == 7)
    .group_by("year_month")
    .agg(pl.count().alias("paper_count"))
    .sort("year_month")
).to_pandas()

# TEMPORAL KPIs
peak_year = papers_by_year.loc[papers_by_year['paper_count'].idxmax()]
peak_month = papers_by_month.loc[papers_by_month['paper_count'].idxmax()]

# Year-over-year growth (last 2 complete years)
recent_years = papers_by_year[papers_by_year['year'].astype(int) >= 2019].tail(3)
if len(recent_years) >= 2:
    yoy_growth = ((recent_years['paper_count'].iloc[-1] - recent_years['paper_count'].iloc[-2]) 
                  / recent_years['paper_count'].iloc[-2] * 100)
else:
    yoy_growth = 0

print("\n[TEMPORAL KPIs]")
print(f"  Total Papers (valid dates): {len(df_temporal):,}")
print(f"  Peak Year: {peak_year['year']} ({peak_year['paper_count']:,} papers)")
print(f"  Peak Month: {peak_month['year_month']} ({peak_month['paper_count']:,} papers)")
print(f"  Recent YoY Growth: {yoy_growth:+.1f}%")

# VISUALIZATION: Papers per Year (Bar Chart)
fig_year = px.bar(
    papers_by_year,
    x='year',
    y='paper_count',
    title='CORD-19: Research Papers Published per Year',
    labels={'year': 'Year', 'paper_count': 'Number of Papers'},
    template=cfg.PLOTLY_TEMPLATE,
    color_discrete_sequence=[cfg.COLOR_PALETTE[0]]
)
fig_year.update_layout(
    xaxis_tickangle=-45,
    showlegend=False,
    height=400
)
fig_year.write_html(cfg.OUTPUT_DIR / "01_papers_per_year.html")
print(f"\n[SAVED] {cfg.OUTPUT_DIR / '01_papers_per_year.html'}")

# VISUALIZATION: Monthly Trend (Line Chart)
fig_month = px.line(
    papers_by_month.tail(60),  # Last 5 years of months
    x='year_month',
    y='paper_count',
    title='CORD-19: Monthly Publication Trend (Recent)',
    labels={'year_month': 'Month', 'paper_count': 'Number of Papers'},
    template=cfg.PLOTLY_TEMPLATE,
)
fig_month.update_traces(line_color=cfg.COLOR_PALETTE[1])
fig_month.update_layout(height=400)
fig_month.write_html(cfg.OUTPUT_DIR / "02_monthly_trend.html")
print(f"[SAVED] {cfg.OUTPUT_DIR / '02_monthly_trend.html'}")

# =============================================================================
# BLOCK 3: JOURNAL ANALYSIS
# =============================================================================
print("\n" + "=" * 70)
print("BLOCK 3: JOURNAL ANALYSIS")
print("=" * 70)

# Clean journal names and count
journal_counts = (
    df
    .filter(pl.col("journal") != "Unknown Journal")
    .filter(pl.col("journal").str.len_chars() > 0)
    .group_by("journal")
    .agg(pl.count().alias("paper_count"))
    .sort("paper_count", descending=True)
)

top_10_journals = journal_counts.head(10).to_pandas()
total_with_journal = journal_counts["paper_count"].sum()

# JOURNAL KPIs
top_journal = top_10_journals.iloc[0]
top_10_total = top_10_journals['paper_count'].sum()
top_10_concentration = (top_10_total / total_with_journal) * 100
unique_journals = journal_counts.height

print("\n[JOURNAL KPIs]")
print(f"  Unique Journals: {unique_journals:,}")
print(f"  Top Journal: {top_journal['journal'][:50]}...")
print(f"    Papers: {top_journal['paper_count']:,}")
print(f"  Top 10 Concentration: {top_10_concentration:.1f}% of all papers")

print("\n[TOP 10 JOURNALS]")
for i, row in top_10_journals.iterrows():
    pct = (row['paper_count'] / total_with_journal) * 100
    print(f"  {i+1}. {row['journal'][:45]}: {row['paper_count']:,} ({pct:.1f}%)")

# VISUALIZATION: Top 10 Journals (Horizontal Bar)
fig_journals = px.bar(
    top_10_journals.iloc[::-1],  # Reverse for horizontal
    y='journal',
    x='paper_count',
    orientation='h',
    title='CORD-19: Top 10 Contributing Journals',
    labels={'journal': 'Journal', 'paper_count': 'Number of Papers'},
    template=cfg.PLOTLY_TEMPLATE,
    color_discrete_sequence=[cfg.COLOR_PALETTE[2]]
)
fig_journals.update_layout(
    height=500,
    yaxis_title="",
    showlegend=False
)
fig_journals.write_html(cfg.OUTPUT_DIR / "03_top_journals.html")
print(f"\n[SAVED] {cfg.OUTPUT_DIR / '03_top_journals.html'}")

# =============================================================================
# BLOCK 4: TEXT MINING (Word Frequency)
# =============================================================================
print("\n" + "=" * 70)
print("BLOCK 4: TEXT MINING (Word Frequency)")
print("=" * 70)

# Sample abstracts for performance
print(f"[INFO] Sampling {cfg.TEXT_SAMPLE_SIZE:,} abstracts for text analysis...")

df_sample = df.filter(
    (pl.col("abstract") != "No Data") &
    (pl.col("abstract").str.len_chars() > 50)
).sample(n=min(cfg.TEXT_SAMPLE_SIZE, len(df)), seed=42)

print(f"[INFO] Sampled {len(df_sample):,} abstracts")

# Tokenize and count words
def extract_words(text):
    """Extract lowercase words, min 3 chars."""
    if not text:
        return []
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return [w for w in words if w not in cfg.STOPWORDS]

# Process abstracts
word_counter = Counter()
abstracts = df_sample["abstract"].to_list()

print("[INFO] Processing word frequencies...")
for i, abstract in enumerate(abstracts):
    if abstract:
        word_counter.update(extract_words(abstract))
    if (i + 1) % 20000 == 0:
        print(f"  Processed {i+1:,} abstracts...")

# Top 30 words
top_words = word_counter.most_common(30)
print(f"\n[TOP 30 KEYWORDS]")
for i, (word, count) in enumerate(top_words[:15], 1):
    print(f"  {i:2}. {word}: {count:,}")

# VISUALIZATION: Word Frequency Bar Chart
word_df = pl.DataFrame({
    "word": [w[0] for w in top_words[:20]],
    "count": [w[1] for w in top_words[:20]]
}).to_pandas()

fig_words = px.bar(
    word_df.iloc[::-1],
    y='word',
    x='count',
    orientation='h',
    title='CORD-19: Top 20 Keywords in Abstracts (Stopwords Removed)',
    labels={'word': 'Keyword', 'count': 'Frequency'},
    template=cfg.PLOTLY_TEMPLATE,
    color_discrete_sequence=[cfg.COLOR_PALETTE[3]]
)
fig_words.update_layout(height=600, yaxis_title="")
fig_words.write_html(cfg.OUTPUT_DIR / "04_word_frequency.html")
print(f"\n[SAVED] {cfg.OUTPUT_DIR / '04_word_frequency.html'}")

# =============================================================================
# BLOCK 5: RESEARCH TREND KPIs
# =============================================================================
print("\n" + "=" * 70)
print("BLOCK 5: RESEARCH TREND KPIs")
print("=" * 70)

def count_trend_papers(df, keywords):
    """Count papers containing any of the keywords in abstract."""
    pattern = "|".join(keywords)
    return df.filter(
        pl.col("abstract").str.to_lowercase().str.contains(pattern)
    ).height

# Calculate trend KPIs
trend_kpis = {}
for trend_name, keywords in cfg.RESEARCH_TRENDS.items():
    count = count_trend_papers(df, keywords)
    pct = (count / total_papers) * 100
    trend_kpis[trend_name] = {"count": count, "percentage": pct}
    print(f"\n[{trend_name.upper()}]")
    print(f"  Papers: {count:,} ({pct:.1f}% of total)")
    print(f"  Keywords: {', '.join(keywords[:5])}...")

# TREND OVER TIME: Calculate monthly trend for each research area
print("\n[INFO] Calculating trend evolution over time...")

df_trends = df_temporal.clone()

for trend_name, keywords in cfg.RESEARCH_TRENDS.items():
    pattern = "|".join(keywords)
    col_name = trend_name.replace(" ", "_").replace("&", "and")
    df_trends = df_trends.with_columns(
        pl.col("abstract")
        .str.to_lowercase()
        .str.contains(pattern)
        .cast(pl.Int32)
        .alias(col_name)
    )

# Aggregate by month
trend_cols = [t.replace(" ", "_").replace("&", "and") for t in cfg.RESEARCH_TRENDS.keys()]
monthly_trends = (
    df_trends
    .filter(pl.col("year_month").str.len_chars() == 7)
    .group_by("year_month")
    .agg([pl.sum(col).alias(col) for col in trend_cols])
    .sort("year_month")
).to_pandas()

# VISUALIZATION: Research Trends Over Time
fig_trends = go.Figure()

colors = [cfg.COLOR_PALETTE[0], cfg.COLOR_PALETTE[1], cfg.COLOR_PALETTE[2]]
for i, (trend_name, col_name) in enumerate(zip(cfg.RESEARCH_TRENDS.keys(), trend_cols)):
    fig_trends.add_trace(go.Scatter(
        x=monthly_trends['year_month'],
        y=monthly_trends[col_name],
        mode='lines',
        name=trend_name,
        line=dict(color=colors[i], width=2)
    ))

fig_trends.update_layout(
    title='CORD-19: Research Trends Over Time',
    xaxis_title='Month',
    yaxis_title='Number of Papers',
    template=cfg.PLOTLY_TEMPLATE,
    height=500,
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)
fig_trends.write_html(cfg.OUTPUT_DIR / "05_research_trends.html")
print(f"\n[SAVED] {cfg.OUTPUT_DIR / '05_research_trends.html'}")

# =============================================================================
# BLOCK 6: EXECUTIVE DASHBOARD (Combined KPIs)
# =============================================================================
print("\n" + "=" * 70)
print("BLOCK 6: EXECUTIVE DASHBOARD")
print("=" * 70)

# Create dashboard with subplots
fig_dashboard = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        'Papers per Year',
        'Top 10 Journals',
        'Research Trend Distribution',
        'Monthly Publication Trend'
    ),
    specs=[
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "pie"}, {"type": "scatter"}]
    ],
    vertical_spacing=0.12,
    horizontal_spacing=0.1
)

# Plot 1: Papers per Year
fig_dashboard.add_trace(
    go.Bar(x=papers_by_year['year'], y=papers_by_year['paper_count'],
           marker_color=cfg.COLOR_PALETTE[0], showlegend=False),
    row=1, col=1
)

# Plot 2: Top 5 Journals
top_5 = top_10_journals.head(5)
fig_dashboard.add_trace(
    go.Bar(y=top_5['journal'].str[:25], x=top_5['paper_count'],
           orientation='h', marker_color=cfg.COLOR_PALETTE[2], showlegend=False),
    row=1, col=2
)

# Plot 3: Research Trends Pie
trend_values = [trend_kpis[t]["count"] for t in cfg.RESEARCH_TRENDS.keys()]
fig_dashboard.add_trace(
    go.Pie(labels=list(cfg.RESEARCH_TRENDS.keys()), values=trend_values,
           marker_colors=colors),
    row=2, col=1
)

# Plot 4: Monthly Trend
recent_months = papers_by_month.tail(36)
fig_dashboard.add_trace(
    go.Scatter(x=recent_months['year_month'], y=recent_months['paper_count'],
               mode='lines', line=dict(color=cfg.COLOR_PALETTE[1]), showlegend=False),
    row=2, col=2
)

fig_dashboard.update_layout(
    title_text='CORD-19 Executive Dashboard',
    height=800,
    template=cfg.PLOTLY_TEMPLATE,
    showlegend=True
)
fig_dashboard.write_html(cfg.OUTPUT_DIR / "06_executive_dashboard.html")
print(f"[SAVED] {cfg.OUTPUT_DIR / '06_executive_dashboard.html'}")

# =============================================================================
# FINAL SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("EDA COMPLETE - SUMMARY")
print("=" * 70)

print(f"""
[KEY FINDINGS]

1. DATASET OVERVIEW
   - Total Papers: {total_papers:,}
   - Unique Journals: {unique_journals:,}
   - Date Range: {papers_by_year['year'].min()} - {papers_by_year['year'].max()}

2. TEMPORAL INSIGHTS
   - Peak Year: {peak_year['year']} ({peak_year['paper_count']:,} papers)
   - Peak Month: {peak_month['year_month']} ({peak_month['paper_count']:,} papers)
   - Recent YoY Growth: {yoy_growth:+.1f}%

3. JOURNAL CONCENTRATION
   - Top Journal: {top_journal['journal'][:40]}
   - Top 10 journals account for {top_10_concentration:.1f}% of papers

4. RESEARCH TRENDS (% of total papers)""")

for trend_name, data in trend_kpis.items():
    print(f"   - {trend_name}: {data['percentage']:.1f}%")

print(f"""
[OUTPUT FILES]
   All visualizations saved to: {cfg.OUTPUT_DIR}/
   - 01_papers_per_year.html
   - 02_monthly_trend.html
   - 03_top_journals.html
   - 04_word_frequency.html
   - 05_research_trends.html
   - 06_executive_dashboard.html

[NEXT STEPS]
   Open any .html file in your browser to view interactive charts.
""")
