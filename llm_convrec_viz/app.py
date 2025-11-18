import streamlit as st
import pandas as pd
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="RA-Rec: Conversational Recommendation",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS FOR ELEGANT LIGHT MODE & CHAT UI ---
st.markdown("""
<style>
    /* General Background & Font */
    .stApp {
        background-color: #FAFAFA;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #333;
    }
    
    /* Card Styling */
    .custom-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #f0f0f0;
    }
    
    /* Highlight Colors for Text */
    .hl-green { color: #27ae60; font-weight: 600; } /* Cuisine/Hard Constraints */
    .hl-purple { color: #8e44ad; font-weight: 600; } /* Vibe/Soft Constraints */
    .hl-blue { color: #2980b9; font-weight: 600; }   /* Dish/Items */
    
    /* Process Visualization Styles */
    .step-box {
        background-color: #fff;
        border-left: 5px solid #4A90E2;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .arrow-down {
        text-align: center;
        font-size: 24px;
        color: #ccc;
        margin: 5px 0;
    }

    /* --- CHAT WINDOW STYLING --- */
    .chat-window {
        max-width: 800px;
        margin: 0 auto;
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
        overflow: hidden;
        font-size: 15px;
    }
    
    .chat-header {
        background-color: #4169E1; /* Royal Blue like screenshot */
        color: white;
        padding: 15px 20px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .chat-body {
        padding: 20px;
        background-color: #fcfcfc;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    
    .bubble {
        padding: 12px 18px;
        border-radius: 18px;
        line-height: 1.5;
        max-width: 80%;
        position: relative;
        margin-bottom: 10px;
    }
    
    /* User Bubble (Right, Blueish) */
    .bubble.user {
        align-self: flex-end;
        background-color: #dceeff; /* Light blue like screenshot */
        color: #0f1e33;
        border-bottom-right-radius: 4px;
    }
    
    /* System Bubble (Left, Grey) */
    .bubble.system {
        align-self: flex-start;
        background-color: #f0f2f5; /* Light grey like screenshot */
        color: #1c1e21;
        border-bottom-left-radius: 4px;
    }

</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
def render_header():
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1 style="font-size: 3.5em; margin-bottom: 10px; font-weight: 700;">RA-Rec</h1>
        <h3 style="font-weight: 300; color: #666;">Retrieval-Augmented Conversational Recommendation with Prompt-based Semi-Structured State</h3>
        <p style="font-size: 1.1em; color: #555; margin-top: 20px;">
            <b>Sara Kemper*, Justin Cui*, Kai Dicarlantonio*, Kathy Lin*, Danjie Tang*</b>, Anton Korikov, Scott Sanner
        </p>
        <p style="font-size: 0.8em; color: #888;">*Equal Contribution | University of Toronto & University of Waterloo | SIGIR '24</p>
        <div style="margin-top: 15px;">
            <a href="https://github.com/D3Mlab/llm-convrec" target="_blank" style="margin-right: 15px; text-decoration: none; color: #4A90E2; font-weight: 600;">GitHub Repository</a>
            <a href="https://arxiv.org/abs/2406.00033" target="_blank" style="text-decoration: none; color: #4A90E2; font-weight: 600;">Read the Paper</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- SECTION 1: CONCEPT & ARCHITECTURE ---
def render_architecture():
    st.markdown("## System Flow")
    st.caption("Explore the pipeline step-by-step.")

    tabs = st.tabs(["1. Intent & State", "2. Retrieval (Deep Dive)", "3. Generation"])

    # --- TAB 1: STATE TRACKING ---
    with tabs[0]:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("#### User Utterance")
            st.markdown("""
            <div class="custom-card">
            "I am looking for <span class="hl-green">Japanese</span> restaurants that serve excellent <span class="hl-blue">sushi</span>, 
            preferably in a <span class="hl-purple">casual setting</span>. I'm <span class="hl-purple">watching my weight</span>."
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("#### Semi-Structured NL State")
            st.markdown("The LLM extracts **Hard Constraints** (mandatory) and **Soft Constraints** (preferences).")
            st.code("""
{
  "hard_constraints": {
    "cuisine_type": ["Japanese"],    // Metadata Filter
    "dish_type": ["sushi"]           // Metadata Filter
  },
  "soft_constraints": {
    "atmosphere": ["casual"],        // Semantic Search
    "others": ["watching my weight"] // Semantic Search
  }
}
            """, language="json")

    # --- TAB 2: RETRIEVAL (DEEP DIVE) ---
    with tabs[1]:
        st.markdown("### Late Fusion Retrieval Process")
        st.markdown("How RA-Rec matches nuance using reviews.")
        
        # STEP 1: HARD FILTER
        st.markdown("#### Step 1: Hard Constraint Filtering")
        st.markdown("First, we filter the database to only include restaurants matching `Japanese` and `Sushi`.")
        
        filter_df = pd.DataFrame({
            "Restaurant": ["Washoku Bistro", "Tokyo Express", "Pasta Place", "Burger King"],
            "Cuisine": ["Japanese", "Japanese", "Italian", "Fast Food"],
            "Status": ["✅ Keep", "✅ Keep", "❌ Discard", "❌ Discard"]
        })
        st.dataframe(filter_df, hide_index=True, use_container_width=True)
        
        st.markdown("<div class='arrow-down'>↓</div>", unsafe_allow_html=True)
        
        # STEP 2: REVIEW SCORING
        st.markdown("#### Step 2: Review-Level Scoring")
        st.markdown("""
        We generate a query and calculate the **Dot Product Similarity** between the query and **ALL reviews** of the remaining restaurants.
        """)
        
        review_data = [
            {"Restaurant": "Washoku Bistro", "Review Text": "Excellent sushi and very fresh.", "Score": 0.93, "Type": "High Match"},
            {"Restaurant": "Washoku Bistro", "Review Text": "Casual atmosphere, great for dates.", "Score": 0.88, "Type": "High Match"},
            {"Restaurant": "Washoku Bistro", "Review Text": "Had many healthy, low-cal options.", "Score": 0.88, "Type": "High Match (Weight)"},
            {"Restaurant": "Tokyo Express", "Review Text": "Love their rolls, very cheap.", "Score": 0.91, "Type": "High Match"},
            {"Restaurant": "Tokyo Express", "Review Text": "Good fried food, a bit greasy.", "Score": 0.62, "Type": "Low Match (Unhealthy)"},
        ]
        df_reviews = pd.DataFrame(review_data)
        
        def highlight_score(val):
            color = '#d4edda' if val > 0.85 else '#f8d7da'
            return f'background-color: {color}'

        st.dataframe(df_reviews.style.applymap(highlight_score, subset=['Score']), use_container_width=True)
        
        st.markdown("<div class='arrow-down'>↓</div>", unsafe_allow_html=True)

        # STEP 3: AGGREGATION
        st.markdown("#### Step 3: Late Fusion Aggregation")
        st.markdown("We average the top-k review scores for each restaurant to get a final **Item Score**.")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            **Washoku Bistro Calculation:**
            $$(0.93 + 0.88 + 0.88) / 3 = \mathbf{0.89}$$
            """)
            st.success("🏆 Winner")
        with col_b:
            st.markdown("""
            **Tokyo Express Calculation:**
            $$(0.91 + 0.87 + 0.80) / 3 = \mathbf{0.86}$$
            """)
            st.warning("🥈 Runner Up")

    # --- TAB 3: GROUNDED GENERATION ---
    with tabs[2]:
        st.markdown("#### Grounded Generation")
        st.markdown("The LLM generates a response using the **Metadata** and the **Top Retrieved Reviews**.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Source Context (Retrieved):**")
            st.markdown("""
            * *Metadata:* Name: Washoku Bistro, Type: Japanese
            * *Review 1:* "Casual atmosphere..."
            * *Review 2:* "Excellent sushi..."
            * *Review 3:* "...low-cal veggie options"
            """)
        
        with col2:
            st.markdown("**Generated Response:**")
            st.markdown("""
            <div class="custom-card" style="background-color: #eaf4fc; border-left: 5px solid #4A90E2;">
            "How about trying <b>Washoku Bistro</b>? 
            It has a <span class="hl-purple">casual</span> vibe and offers 
            <span class="hl-green">low-calorie menu items</span> (from review 3) 
            while serving excellent <span class="hl-blue">Japanese sushi</span>."
            </div>
            """, unsafe_allow_html=True)

# --- SECTION 2: STATIC CONVERSATION UI ---
def render_chat_demo():
    st.markdown("---")
    st.markdown("## Example Conversation")
    st.caption("A full dialogue demonstrating preference understanding, rejection, and QA.")

    # IMPORTANT: Left-aligned HTML to prevent Markdown code-block interpretation
    chat_html = """
<div class="chat-window">
<div class="chat-header">
<span>📍 Restaurant Finder</span>
</div>
<div class="chat-body">

<div class="bubble user">
I am looking for <span class="hl-green">Japanese</span> restaurants that serve excellent <span class="hl-blue">sushi</span>, preferably in a <span class="hl-purple">casual setting</span>.
</div>
<div class="bubble system">
Can you provide the location?
</div>

<div class="bubble user">
Tower Road NW & Kingsway NW
</div>
<div class="bubble system">
How about trying Washoku Bistro for a <span class="hl-purple">comfortable and laid-back vibe</span> while enjoying some delicious <span class="hl-green">Japanese</span> <span class="hl-blue">sushi</span>? But if you're looking for something quick and easy without sacrificing taste, Tokyo Express is another great option near the same location.
</div>

<div class="bubble user">
What kind of menu do they offer?
</div>
<div class="bubble system">
For Washoku Bistro, they offer a lunch menu with bento boxes and entrées, with limited options. They also have <span class="hl-blue">sushi rolls</span>, such as spicy salmon rolls and California rolls. As for Tokyo Express, they have a wide variety of options including bento boxes, <span class="hl-blue">sushi combos</span>, feature rolls, tempura, and noodles.
</div>

<div class="bubble user">
Ok, then the first one doesn't seem to match my preference.
</div>
<div class="bubble system">
I'm sorry that you did not like the recommendation. Is there anything else I can assist you with?
</div>

<div class="bubble user">
Does Tokyo Express have a parking lot?
</div>
<div class="bubble system">
Tokyo Express has a parking lot.
</div>

<div class="bubble user">
Great. I will go there then. Thanks!
</div>
<div class="bubble system">
Great! Enjoy your meal! If you need any more assistance, feel free to ask.
</div>
</div>
</div>
"""
    
    st.markdown(chat_html, unsafe_allow_html=True)

# --- MAIN EXECUTION ---
render_header()
render_architecture()
render_chat_demo()

# --- FOOTER ---
st.markdown("""
<br><br>
<div style="text-align: center; color: #aaa; font-size: 0.8em;">
    Paper: <a href="https://arxiv.org/abs/2406.00033" style="color: #aaa;">arXiv:2406.00033</a> [cs.CL] <br>
    Demo built with Streamlit • 2025
</div>
""", unsafe_allow_html=True)