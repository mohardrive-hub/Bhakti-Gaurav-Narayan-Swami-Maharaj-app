import streamlit as st
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="Maharaj Lectures", page_icon="🕉️", layout="wide")

# 2. Advanced CSS to Force Light Mode and App Styling
st.markdown("""
    <style>
    /* FORCE LIGHT MODE COLORS */
    :root {
        --primary-color: #E65100;
        --background-color: #FFF9F2;
        --secondary-background-color: #FFF3E0;
        --text-color: #3E2723;
        --font: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Main Background */
    .stApp { 
        background-color: #FFF9F2 !important; 
    }
    
    /* Force text color globally */
    h1, h2, h3, p, span, div {
        color: #3E2723 !important;
    }

    /* Card Styling - Mobile Optimized */
    .lecture-card {
        background: white !important;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #FFE0B2;
    }
    
    /* Title Styling */
    .lecture-title {
        color: #BF360C !important;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 5px;
        line-height: 1.3;
    }
    
    /* Metadata Pills */
    .pill {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 15px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-right: 4px;
        margin-bottom: 4px;
        background: #FBE9E7 !important;
        color: #D84315 !important;
        border: 0.5px solid #FFCCBC;
    }

    /* Sidebar text fix */
    section[data-testid="stSidebar"] {
        background-color: #FFF3E0 !important;
    }
    
    /* Button Styling Override */
    .stButton>button {
        border-radius: 8px;
        border: 1px solid #FFCCBC;
        background-color: white;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #E65100;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        return pd.read_csv("Maharaj_Perfect_Metadata.csv")
    except:
        return pd.DataFrame()

df = load_data()

# --- HEADER ---
st.markdown("<h2 style='text-align: center; color: #E65100; margin-bottom: 0;'>🙏 Bhakti Gaurav Narayan Swami</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #5D4037; font-size: 0.9rem;'>Official Audio Library</p>", unsafe_allow_html=True)

# --- SIDEBAR FILTERS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2903/2903513.png", width=60)
st.sidebar.markdown("### 🔍 Quick Search")
search_query = st.sidebar.text_input("", placeholder="Topic, Place, Verse...")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Filter By")
selected_year = st.sidebar.multiselect("Year", sorted(df['Year'].unique(), reverse=True))
selected_lang = st.sidebar.multiselect("Language", df['Language'].unique(), default=df['Language'].unique())
selected_type = st.sidebar.radio("Category", ["All"] + list(df['Type'].unique()))

# --- LOGIC ---
filtered_df = df[df['Language'].isin(selected_lang)]
if selected_year:
    filtered_df = filtered_df[filtered_df['Year'].isin(selected_year)]
if selected_type != "All":
    filtered_df = filtered_df[filtered_df['Type'] == selected_type]
if search_query:
    filtered_df = filtered_df[filtered_df['File Name'].str.contains(search_query, case=False, na=False)]

# --- MAIN LIST ---
st.caption(f"Found {len(filtered_df)} lectures")

for i, row in filtered_df.iterrows():
    # Extract Drive ID for buttons
    source_url = str(row['Source Link'])
    file_id = source_url.split('id=')[-1].split('&')[0] if 'id=' in source_url else ""
    preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
    
    with st.container():
        st.markdown(f"""
            <div class="lecture-card">
                <div class="lecture-title">{row['Code']}</div>
                <div style="margin-top: 5px;">
                    <span class="pill">🌍 {row['Language']}</span>
                    <span class="pill">📍 {row['Location']}</span>
                    <span class="pill">📅 {row['Year']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Action Buttons for Mobile (Stacked)
        c1, c2, c3 = st.columns([1.5, 1, 1])
        with c1:
            st.link_button("▶️ Listen", preview_url, use_container_width=True)
        with c2:
            st.link_button("📥 Save", source_url, use_container_width=True)
        with c3:
            share_text = f"Maharaj Lecture: {row['Code']} - {preview_url}"
            st.link_button("🔗 WhatsApp", f"https://wa.me/?text={share_text}", use_container_width=True)
        st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
