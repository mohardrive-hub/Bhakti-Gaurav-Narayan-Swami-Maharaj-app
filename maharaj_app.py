import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Maharaj Audio App", page_icon="🙏", layout="wide")

# Custom CSS for a professional, easy-to-read interface
st.markdown("""
    <style>
    .main { background-color: #f7f9fc; }
    .lecture-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #ff9933;
        margin-bottom: 20px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    }
    .lecture-title {
        color: #1e293b !important;
        font-weight: 700;
        font-size: 1.25em;
        margin-bottom: 8px;
        line-height: 1.4;
    }
    .lecture-tag {
        display: inline-block;
        background: #fff3e0;
        color: #e65100;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        margin-right: 8px;
    }
    .info-text {
        color: #64748b;
        font-size: 0.9em;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        # Loading the metadata file
        return pd.read_csv("Maharaj_Perfect_Metadata.csv")
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None

df = load_data()

if df is not None:
    # --- Sidebar Filters ---
    st.sidebar.header("🙏 App Filters")
    search_query = st.sidebar.text_input("🔍 Search Topic / Verse", placeholder="E.g. Puri, SB 1.1...")
    
    selected_lang = st.sidebar.multiselect("Language", options=df['Language'].unique(), default=df['Language'].unique())
    selected_year = st.sidebar.multiselect("Year", options=sorted(df['Year'].unique(), reverse=True))
    selected_type = st.sidebar.multiselect("Category", options=df['Type'].unique(), default=df['Type'].unique())

    # --- Filtering Logic ---
    filtered_df = df[
        (df['Language'].isin(selected_lang)) & 
        (df['Type'].isin(selected_type))
    ]
    
    if selected_year:
        filtered_df = filtered_df[filtered_df['Year'].isin(selected_year)]
        
    if search_query:
        mask = (
            filtered_df['File Name'].str.contains(search_query, case=False, na=False) |
            filtered_df['Code'].str.contains(search_query, case=False, na=False) |
            filtered_df['Location'].str.contains(search_query, case=False, na=False)
        )
        filtered_df = filtered_df[mask]

    # --- Header ---
    st.title("🙏 Maharaj Audio Library")
    st.write(f"Showing **{len(filtered_df)}** lectures")

    # --- Display Lectures ---
    for i, row in filtered_df.iterrows():
        # Correctly extract the Drive ID for the player
        # Handles various link formats
        source_url = str(row['Source Link'])
        file_id = ""
        if "id=" in source_url:
            file_id = source_url.split('id=')[-1].split('&')[0]
        elif "file/d/" in source_url:
            file_id = source_url.split('file/d/')[-1].split('/')[0]

        # Different formats for different needs
        stream_url = f"https://drive.google.com/uc?id={file_id}&export=download"
        preview_url = f"https://drive.google.com/file/d/{file_id}/preview"

        with st.container():
            st.markdown(f"""
                <div class="lecture-card">
                    <div class="lecture-title">{row['Code']}</div>
                    <div>
                        <span class="lecture-tag">{row['Language']}</span>
                        <span class="lecture-tag">{row['Type']}</span>
                        <span class="info-text">📍 {row['Location']} | 📅 {row['Date']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # 1. The Direct Audio Player (Works if Drive allows)
            st.audio(stream_url, format="audio/mp3")
            
            # 2. Control Buttons for Devotees
            col1, col2 = st.columns(2)
            with col1:
                # This opens Google's built-in player which ALWAYS works
                st.link_button("▶️ Play Audio (Stable)", preview_url, use_container_width=True)
            with col2:
                # The direct download link
                st.link_button("📥 Download MP3", source_url, use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
else:
    st.warning("CSV Data could not be loaded. Check your GitHub repository.")
