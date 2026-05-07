import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Maharaj App MVP", page_icon="🙏", layout="wide")

# Modern UI Styling
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stAudio { margin-top: 10px; }
    .lecture-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-top: 4px solid #ff9933;
        margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    .lecture-title {
        color: #2c3e50 !important;
        font-weight: 700;
        font-size: 1.3em;
        margin-bottom: 8px;
    }
    .lecture-tag {
        display: inline-block;
        background: #fff3e0;
        color: #e65100;
        padding: 2px 10px;
        border-radius: 15px;
        font-size: 0.8em;
        font-weight: bold;
        margin-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("Maharaj_Perfect_Metadata.csv")

try:
    df = load_data()

    # --- FANCY SIDEBAR ---
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2903/2903513.png", width=100)
    st.sidebar.title("App Settings")
    
    st.sidebar.markdown("---")
    search_query = st.sidebar.text_input("🔍 Search Anything", placeholder="E.g. Puri, Seminar, SB...")
    
    st.sidebar.subheader("🎯 Quick Filters")
    selected_lang = st.sidebar.multiselect("Language", options=df['Language'].unique(), default=df['Language'].unique())
    selected_year = st.sidebar.multiselect("Year", options=sorted(df['Year'].unique(), reverse=True))
    selected_type = st.sidebar.multiselect("Category", options=df['Type'].unique(), default=df['Type'].unique())

    # --- FILTERING LOGIC ---
    filtered_df = df[
        (df['Language'].isin(selected_lang)) & 
        (df['Type'].isin(selected_type))
    ]
    
    if selected_year:
        filtered_df = filtered_df[filtered_df['Year'].isin(selected_year)]
        
    if search_query:
        # Search across multiple columns
        mask = (
            filtered_df['File Name'].str.contains(search_query, case=False) |
            filtered_df['Code'].str.contains(search_query, case=False) |
            filtered_df['Location'].str.contains(search_query, case=False)
        )
        filtered_df = filtered_df[mask]

    # --- MAIN DISPLAY ---
    st.title("🙏 Maharaj Audio Library")
    st.caption(f"Showing {len(filtered_df)} of {len(df)} lectures")

    for i, row in filtered_df.iterrows():
        # DEBUG/FIX: Converting 'export=download' to 'open' for better browser streaming
        # Some browsers block 'download' links in audio tags
        streaming_url = row['Source Link'].replace("export=download", "open")
        
        with st.container():
            st.markdown(f"""
                <div class="lecture-card">
                    <div class="lecture-title">{row['Code']}</div>
                    <div>
                        <span class="lecture-tag">{row['Language']}</span>
                        <span class="lecture-tag">{row['Type']}</span>
                        <span style="color:#7f8c8d; font-size:0.9em;">📍 {row['Location']} | 📅 {row['Date']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # The Player
            st.audio(streaming_url)
            
            # Sub-menu for downloading
            col1, col2 = st.columns([1, 4])
            with col1:
                st.link_button("📥 Save MP3", row['Source Link'], use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)

except Exception as e:
    st.sidebar.error(f"Config Error: {e}")