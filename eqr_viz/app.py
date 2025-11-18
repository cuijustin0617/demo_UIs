import streamlit as st
import pandas as pd
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EQR: Elaborative Query Reformulation",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #FAFAFA;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #333;
    }
    
    /* Title & Headers */
    h1, h2, h3 { font-weight: 700; letter-spacing: -0.5px; color: #111; }
    
    /* Custom Cards */
    .method-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        height: 100%;
    }
    
    /* Reformulation Text Styling */
    .ref-box {
        background-color: #f8f9fa;
        border-left: 4px solid #ccc;
        padding: 10px 15px;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
        margin-bottom: 10px;
    }
    .ref-box.eqr { border-left-color: #4A90E2; background-color: #eef6fc; }
    .ref-box.q2e { border-left-color: #eb3b5a; }
    .ref-box.q2d { border-left-color: #20bf6b; }

    /* Ranking List Styling */
    .rank-item {
        padding: 8px 12px;
        border-bottom: 1px solid #eee;
        display: flex;
        justify-content: space-between;
    }
    .rank-item:last-child { border-bottom: none; }
    .rank-score { color: #888; font-size: 0.85em; }
    .rank-ideal { background-color: #d4edda; border-radius: 5px; color: #155724; }
    .rank-bad { background-color: #f8d7da; border-radius: 5px; color: #721c24; }

    /* Highlight Classes */
    .breadth { color: #d35400; font-weight: 600; }
    .depth { color: #2980b9; font-weight: 600; }
    
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
def render_header():
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1 style="font-size: 3em; margin-bottom: 10px;">EQR</h1>
        <h3 style="font-weight: 300; color: #555;">A Simple but Effective Elaborative Query Reformulation Approach For Natural Language Recommendation</h3>
        <p style="font-size: 1.1em; color: #444; margin-top: 15px;">
            <b>Qianfeng Wen*, Yifan Liu*, Justin Cui*</b>, Joshua Zhang, Anton Korikov, George-Kirollos Saad, Scott Sanner
        </p>
        <p style="font-size: 0.9em; color: #888;">*Equal Contribution | University of Toronto | arXiv:2510.02656 [cs.IR]</p>
    </div>
    """, unsafe_allow_html=True)

# --- PROBLEM DEFINITION ---
def render_problem():
    st.markdown("### The Challenge: Broad & Indirect Queries")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.info("**The Input**")
        st.markdown("""
        Users often ask **Broad** or **Indirect** queries:
        * *"Cities for youth-friendly activities"* (Broad)
        * *"Cities for a high school graduation trip"* (Indirect)
        
        Standard retrieval struggles to map these high-level concepts to specific item descriptions.
        """)
        
    with col2:
        st.success("**The Solution (EQR)**")
        st.markdown("""
        Effective recommendation requires two dimensions:
        1.  <span class="breadth">Breadth:</span> Covering diverse subtopics (e.g., Nightlife, Budget, Outdoors).
        2.  <span class="depth">Depth:</span> Elaborating on *why* those subtopics matter.
        
        **EQR** uses an LLM to generate both.
        """, unsafe_allow_html=True)

# --- INTERACTIVE DEMO ---
def render_demo():
    st.markdown("---")
    st.markdown("## 🔍 Interactive Comparison")
    st.caption("Select a query to see how different reformulation methods affect retrieval results.")
    
    # Pre-defined scenarios based on the paper
    scenarios = {
        "Cities for youth-friendly activities": {
            "q2e_text": "Night life; Budget hotels; Outdoor activities; Hostels; Backpacking; Cheap eats; Bars; Clubs",
            "q2d_text": "Amsterdam is a vibrant city known for its lively nightlife and strong youth culture. It offers numerous hostels...",
            "eqr_text": """1. Night life: Cities with live music venues, diverse night markets...
2. Budget hotels: Cities with budget-friendly lodging options...
3. Outdoor activities: Cities with lots of biking trails, beaches...""",
            "q2e_ranks": [("1. Amsterdam", "0.85"), ("2. Bucharest", "0.84 (Cheap but not youth focused)"), ("...", ""), ("56. Bangkok", "0.62")],
            "q2d_ranks": [("1. Amsterdam", "0.88"), ("...", ""), ("73. Vancouver", "0.55 (Missed outdoor aspect)"), ("...", "")],
            "eqr_ranks": [("1. Amsterdam", "0.89"), ("2. Bangkok", "0.82"), ("3. Vancouver", "0.80"), ("...", "")]
        },
        "Cities for a high school graduation trip": {
            "q2e_text": "youth-friendly activities; budget accommodations; group tours; adventure parks; cultural experiences",
            "q2d_text": "New York City, USA: As one of the world's most iconic destinations, NYC offers a dynamic setting for graduation trips...",
            "eqr_text": """1. Adventure Activities: Cities offering exciting outdoor activities... (e.g. Queenstown)
2. Cultural Hotspots: Cities rich in museums and history... (e.g. Rome)
3. Beach Destinations: Vibrant beach scenes suitable for young travelers... (e.g. Miami)""",
            "q2e_ranks": [("1. Aarhus", "0.81"), ("2. San Francisco", "0.79"), ("...", "")],
            "q2d_ranks": [("1. New York City", "0.86"), ("2. London", "0.84"), ("...", "")],
            "eqr_ranks": [("1. Queenstown", "0.88"), ("2. New York City", "0.85"), ("3. Rome", "0.82")]
        }
    }

    query_selection = st.selectbox("Choose a User Query:", list(scenarios.keys()))
    data = scenarios[query_selection]

    # --- VISUALIZATION COLUMNS ---
    col1, col2, col3 = st.columns(3)

    # METHOD 1: Q2E
    with col1:
        st.markdown("#### Q2E (Breadth Only)")
        st.caption("Query2Expansion")
        with st.container():
            st.markdown(f'<div class="ref-box q2e">{data["q2e_text"]}</div>', unsafe_allow_html=True)
            st.markdown("**Result:** Expands keywords but lacks context. Can retrieve superficially matching items.")
            st.markdown("---")
            for rank, score in data["q2e_ranks"]:
                color_class = "rank-bad" if "Bucharest" in rank or "Aarhus" in rank else ""
                st.markdown(f'<div class="rank-item {color_class}"><span>{rank}</span><span class="rank-score">{score}</span></div>', unsafe_allow_html=True)

    # METHOD 2: Q2D
    with col2:
        st.markdown("#### Q2D (Depth Only)")
        st.caption("Query2Doc")
        with st.container():
            st.markdown(f'<div class="ref-box q2d">{data["q2d_text"]}</div>', unsafe_allow_html=True)
            st.markdown("**Result:** Focuses deeply on one interpretation (Tunnel Vision). Misses other relevant items.")
            st.markdown("---")
            for rank, score in data["q2d_ranks"]:
                st.markdown(f'<div class="rank-item"><span>{rank}</span><span class="rank-score">{score}</span></div>', unsafe_allow_html=True)

    # METHOD 3: EQR (OURS)
    with col3:
        st.markdown("#### EQR (Breadth + Depth)")
        st.caption("Elaborative Subtopic QR")
        with st.container():
            st.markdown(f'<div class="ref-box eqr">{data["eqr_text"]}</div>', unsafe_allow_html=True)
            st.markdown("**Result:** Breaks query into subtopics AND elaborates on them. Retrieves diverse, relevant items.")
            st.markdown("---")
            for rank, score in data["eqr_ranks"]:
                st.markdown(f'<div class="rank-item rank-ideal"><span>{rank}</span><span class="rank-score">{score}</span></div>', unsafe_allow_html=True)

# --- PIPELINE VISUALIZATION ---
def render_pipeline():
    st.markdown("---")
    st.markdown("## ⚙️ The EQR Pipeline")
    
    st.write("How EQR converts a raw user query into a ranked list.")
    

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**1. Input Query**")
        st.info("Cities for youth-friendly activities")
    
    with col2:
        st.markdown("**2. LLM Reformulation**")
        st.markdown("""
        Prompt the LLM to:
        1. Identify **Subtopics** (Breadth)
        2. Provide **Elaborations** (Depth)
       
        """)
    
    with col3:
        st.markdown("**3. Dense Retrieval**")
        st.write("We encode the reformulated query and search against passage embeddings.")
    
    with col4:
        st.markdown("**4. Aggregation**")
        st.success("Average the top-k passage scores to rank items (Late Fusion).")

# --- DATASETS ---
def render_datasets():
    st.markdown("---")
    st.markdown("## 📂 Natural Language Query-Driven Recommendation Datasets")
    st.markdown("""
    We provide three natural language query-driven recommendation datasets designed to evaluate systems under challenging conditions where:
    
    1. User intent is **implicitly expressed** through broad or indirect queries
    2. Items are described through **multiple diverse textual sources**
    
    Each dataset contains 100 natural language queries, ground truth relevance labels, and original corpus of items for reference.
    
    🤗 **[Access the datasets on Hugging Face](https://huggingface.co/datasets/cuijustin0617/NLRec)**
    """)
    
    df = pd.DataFrame({
        "Dataset": ["Yelp Restaurant", "TripAdvisor Hotel", "Traveldest"],
        "Cities/Categories": [
            "New Orleans (nor), Philadelphia (phi)",
            "New York City, Chicago, London, Montreal",
            "/"
        ],
        "Corpus Size": [
            "1,152 restaurants (nor: 515, phi: 637)",
            "586 hotels (nyc: 182, chicago: 74, london: 266, montreal: 64)",
            "775 cities"
        ],
        "Queries": [100, 100, 100]
    })
    
    st.table(df)
    
    # Detailed dataset descriptions
    st.markdown("### Dataset Details")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Yelp Restaurant")
        st.markdown("""
        Restaurant recommendations based on Yelp reviews:
        - 100 natural language queries
        - Ground truth relevance labels for New Orleans and Philadelphia
        - 1,152 restaurants organized by city
        """)
    
    with col2:
        st.markdown("#### TripAdvisor Hotel")
        st.markdown("""
        Hotel recommendations based on TripAdvisor reviews:
        - 100 natural language queries
        - Ground truth relevance labels for NYC, Chicago, London, and Montreal
        - 586 hotels organized by city
        """)
    
    with col3:
        st.markdown("#### Traveldest")
        st.markdown("""
        Travel destination recommendations based on WikiVoyage pages:
        - 100 natural language queries
        - Ground truth relevance labels for various cities
        - 775 cities with detailed WikiVoyage descriptions
        """)


# --- MAIN APP ---
render_header()
render_problem()
render_demo()
render_pipeline()
render_datasets()

st.markdown("""
<div style="text-align: center; margin-top: 50px; color: #aaa; font-size: 0.8em;">
    Based on arXiv:2510.02656v2 • 2025
</div>
""", unsafe_allow_html=True)