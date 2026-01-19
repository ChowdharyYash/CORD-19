"""
dashboard.py - Interactive CORD-19 Drug Analysis Dashboard
==========================================================
Run with: streamlit run dashboard.py

Features:
1. Top Efficacies - Most frequently mentioned drug efficacies
2. Top Chemicals for X - Highest occurring drugs for selected efficacy
3. Efficacies of Drugs Co-Occurring with X - Drug combinations analysis
4. Efficacies Sharing Chemicals with X - Multi-efficacy drug labels
5. Chemical Timeline - Yearly % of papers mentioning drug
6. Monthly Change in Paper Count - Month-over-month trend
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from drug_miner import build_drug_cache, DrugMiner
from drug_dictionary import DRUG_EFFICACY_MAP, get_all_drugs, get_all_efficacies

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="CORD-19 Drug Analysis",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# LOAD DATA (cached)
# =============================================================================
@st.cache_resource
def load_miner():
    """Load drug miner with caching."""
    return build_drug_cache(force_rebuild=False)

# Load data
with st.spinner("Loading drug analysis data..."):
    miner = load_miner()

# =============================================================================
# SIDEBAR
# =============================================================================
st.sidebar.title("CORD-19 Drug Analysis")
st.sidebar.markdown("---")

# Get available drugs and efficacies (only those with mentions)
available_drugs = [d for d, c in miner.get_top_drugs(100) if c > 0]
available_efficacies = [e for e, c in miner.get_top_efficacies(50) if c > 0]

# Selection widgets
st.sidebar.subheader("Select Drug")
selected_drug = st.sidebar.selectbox(
    "Choose a drug compound:",
    options=available_drugs,
    index=0 if available_drugs else None
)

st.sidebar.subheader("Select Efficacy")
selected_efficacy = st.sidebar.selectbox(
    "Choose an efficacy type:",
    options=available_efficacies,
    index=0 if available_efficacies else None
)

st.sidebar.markdown("---")
st.sidebar.info(f"Dataset: ~970K papers\nDrugs tracked: {len(DRUG_EFFICACY_MAP)}")

# =============================================================================
# MAIN DASHBOARD
# =============================================================================
st.title("CORD-19 Drug & Chemical Analysis Dashboard")
st.markdown("Interactive analysis of drug/chemical mentions in COVID-19 research papers")

# =============================================================================
# ROW 1: Top Efficacies & Top Chemicals for Efficacy
# =============================================================================
col1, col2 = st.columns(2)

# --- CHART 1: Top Efficacies ---
with col1:
    st.subheader("Top Efficacies")
    st.caption("Most frequently mentioned drug efficacies in CORD-19")
    
    top_eff = miner.get_top_efficacies(15)
    if top_eff:
        df_eff = pd.DataFrame(top_eff, columns=["Efficacy", "Mentions"])
        
        fig1 = px.bar(
            df_eff.iloc[::-1],
            y="Efficacy",
            x="Mentions",
            orientation="h",
            color="Mentions",
            color_continuous_scale="Blues"
        )
        fig1.update_layout(height=450, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("No efficacy data available")

# --- CHART 2: Top Chemicals for Selected Efficacy ---
with col2:
    st.subheader(f"Top Chemicals for: {selected_efficacy}")
    st.caption(f"Drugs with '{selected_efficacy}' efficacy label")
    
    if selected_efficacy:
        drugs_for_eff = miner.get_drugs_for_efficacy(selected_efficacy, n=12)
        
        if drugs_for_eff:
            df_drugs = pd.DataFrame(drugs_for_eff, columns=["Drug", "Mentions"])
            
            fig2 = px.bar(
                df_drugs.iloc[::-1],
                y="Drug",
                x="Mentions",
                orientation="h",
                color="Mentions",
                color_continuous_scale="Greens"
            )
            fig2.update_layout(height=450, showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info(f"No drugs found with efficacy '{selected_efficacy}'")

st.markdown("---")

# =============================================================================
# ROW 2: Co-occurring Efficacies & Shared Efficacies
# =============================================================================
col3, col4 = st.columns(2)

# --- CHART 3: Efficacies of Drugs Co-Occurring with Selected Drug ---
with col3:
    st.subheader(f"Efficacies Co-Occurring with: {selected_drug}")
    st.caption("Efficacies of drugs mentioned together with selected drug")
    
    if selected_drug:
        cooccur_eff = miner.get_cooccurring_efficacies(selected_drug, is_drug=True, n=12)
        
        if cooccur_eff:
            df_cooccur = pd.DataFrame(cooccur_eff, columns=["Efficacy", "Co-occurrences"])
            
            fig3 = px.bar(
                df_cooccur.iloc[::-1],
                y="Efficacy",
                x="Co-occurrences",
                orientation="h",
                color="Co-occurrences",
                color_continuous_scale="Oranges"
            )
            fig3.update_layout(height=400, showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info(f"No co-occurrence data for '{selected_drug}'")

# --- CHART 4: Efficacies Sharing Chemicals (Multi-label drugs) ---
with col4:
    st.subheader(f"All Efficacies of: {selected_drug}")
    st.caption("Multiple efficacy labels for selected drug compound")
    
    if selected_drug:
        shared_effs = miner.get_shared_efficacies(selected_drug)
        
        if shared_effs:
            # Create a simple display
            df_shared = pd.DataFrame({
                "Efficacy": shared_effs,
                "Label": [1] * len(shared_effs)
            })
            
            fig4 = px.bar(
                df_shared,
                x="Efficacy",
                y="Label",
                color="Efficacy",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig4.update_layout(
                height=400, 
                showlegend=False,
                yaxis_title="",
                yaxis_showticklabels=False
            )
            fig4.update_traces(width=0.6)
            st.plotly_chart(fig4, use_container_width=True)
            
            # Also show as list
            st.markdown("**Efficacy Labels:**")
            for eff in shared_effs:
                st.markdown(f"- {eff.title()}")
        else:
            st.info(f"No efficacy data for '{selected_drug}'")

st.markdown("---")

# =============================================================================
# ROW 3: Chemical Timeline
# =============================================================================
st.subheader(f"Chemical Timeline: {selected_drug}")
st.caption("Percentage of papers mentioning drug per year (normalized by total papers)")

if selected_drug:
    timeline = miner.get_drug_timeline(selected_drug)
    
    if timeline:
        df_timeline = pd.DataFrame(timeline)
        df_timeline = df_timeline[df_timeline["year"].str.isdigit()]
        df_timeline = df_timeline[df_timeline["year"].astype(int) >= 2010]
        
        if not df_timeline.empty:
            fig5 = go.Figure()
            
            # Bar for absolute count
            fig5.add_trace(go.Bar(
                x=df_timeline["year"],
                y=df_timeline["papers"],
                name="Paper Count",
                marker_color="lightblue",
                yaxis="y"
            ))
            
            # Line for percentage
            fig5.add_trace(go.Scatter(
                x=df_timeline["year"],
                y=df_timeline["percentage"],
                name="% of Papers",
                mode="lines+markers",
                line=dict(color="red", width=3),
                marker=dict(size=8),
                yaxis="y2"
            ))
            
            fig5.update_layout(
                height=400,
                yaxis=dict(title="Paper Count", side="left"),
                yaxis2=dict(title="% of Total Papers", side="right", overlaying="y"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
                hovermode="x unified"
            )
            
            st.plotly_chart(fig5, use_container_width=True)
        else:
            st.info("No timeline data available")

st.markdown("---")

# =============================================================================
# ROW 4: Monthly Change in Paper Count
# =============================================================================
st.subheader(f"Monthly Change in Paper Count: {selected_drug}")
st.caption("Month-over-month change in papers mentioning the drug")

if selected_drug:
    monthly = miner.get_monthly_change(selected_drug)
    
    if monthly and len(monthly) > 1:
        df_monthly = pd.DataFrame(monthly)
        # Filter to recent months with data
        df_monthly = df_monthly[df_monthly["count"] > 0].tail(36)
        
        if not df_monthly.empty:
            # Color by positive/negative change
            colors = ["green" if x >= 0 else "red" for x in df_monthly["change"]]
            
            fig6 = go.Figure()
            
            # Bar for absolute change
            fig6.add_trace(go.Bar(
                x=df_monthly["month"],
                y=df_monthly["change"],
                name="Change",
                marker_color=colors
            ))
            
            fig6.update_layout(
                height=400,
                xaxis_tickangle=-45,
                yaxis_title="Change from Previous Month",
                hovermode="x unified"
            )
            
            st.plotly_chart(fig6, use_container_width=True)
            
            # Show summary stats
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                total_mentions = df_monthly["count"].sum()
                st.metric("Total Mentions (shown period)", f"{total_mentions:,}")
            with col_b:
                avg_change = df_monthly["change"].mean()
                st.metric("Avg Monthly Change", f"{avg_change:+.1f}")
            with col_c:
                peak_month = df_monthly.loc[df_monthly["count"].idxmax()]
                st.metric("Peak Month", f"{peak_month['month']}")
        else:
            st.info("Insufficient monthly data")

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <small>
        CORD-19 Drug Analysis Dashboard | Data: AI2 Semantic Scholar | 
        Built with Streamlit & Plotly
    </small>
</div>
""", unsafe_allow_html=True)
