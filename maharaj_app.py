import streamlit as st
import pandas as pd

# 1. Page Configuration (Centered layout acts more like a mobile feed on laptops)
st.set_page_config(page_title="Maharaj Audio App", page_icon="🕉️", layout="centered", initial_sidebar_state="collapsed")

# 2. Premium Custom CSS
st.markdown("""
    <style>
    /* Force Light Theme Background */
    .stApp {
        background-color: #F8F9FB !important;
    }
    
    /* Hide Streamlit Clutter for Native App Feel */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Typography & Colors */
    h1, h2, h3, p, span, div {
        color: #202124 !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Search Input Styling */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 1px solid #E0E0E0 !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05) !important;
    }

    /* Lecture Card Styling */
    .lecture-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #F0F0F0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .lecture-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    }

    /* Title Inside Card */
    .card-title {
        color: #D84315 !important; /* Deep Saffron */
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 12px;
        line-height: 1.4;
    }

    /* Metadata Pills */
    .badge {
        background-color: #FFF3E0 !important;
        color: #E65100 !important;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 8px;
        margin-bottom: 8px;
        border: 1px solid #FFE0B2;
    }
    
    .meta-text {
        color: #5F6368 !important;
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 8px;
    }

    /* Button Overrides - Prevent the Black/White Flash */
    .stButton > button, .stDownloadButton > button, a[data-testid="stLinkButton"] {
        background-color: #FFFFFF !important;
        color: #E65100 !important;
        border: 1px solid #E65100 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover, .stDownloadButton > button:hover, a[data-testid="stLinkButton"]:hover {
        background-color: #E65100 !important;
        color: #FFFFFF !important;
        border-color: #E65100 !important;
    }

    /* Divider */
    hr {
        border-top: 1px solid #EAEAEA;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Load Data Safely
@st.cache_data
def load_data():
    try:
        return pd.read_csv("Maharaj_Perfect_Metadata.csv")
    except Exception as e:
        return pd.DataFrame() # Return empty if error

df = load_data()

# 4. APP UI - HEADER
st.markdown("""
    <div style="text-align: center; padding: 20px 0 10px 0;">
        <h1 style="color: #D84315 !important; font-size: 2rem; margin-bottom: 5px;">🙏 Audio Library</h1>
        <p style="color: #5F6368 !important; font-size: 0.9rem;">HH Bhakti Gaurav Narayan Swami Maharaj</p>
    </div>
""", unsafe_allow_html=True)

if not df.empty:
    # 5. SEARCH & FILTERS
    search_query = st.text_input("Search", placeholder="🔍 Find a topic, place, or verse...", label_visibility="collapsed")
    
    with st.expander("⚙️ Advanced Filters"):
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_lang = st.multiselect("Language", df['Language'].unique())
        with col2:
            years = sorted([y for y in df['Year'].unique() if pd.notna(y)], reverse=True)
            selected_year = st.multiselect("Year", years)
        with col3:
            selected_type = st.multiselect("Category", df['Type'].unique())

    # --- FILTERING LOGIC ---
    filtered_df = df.copy()
    if search_query:
        mask = (
            filtered_df['File Name'].str.contains(search_query, case=False, na=False) |
            filtered_df['Code'].str.contains(search_query, case=False, na=False) |
            filtered_df['Location'].str.contains(search_query, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    if selected_lang:
        filtered_df = filtered_df[filtered_df['Language'].isin(selected_lang)]
    if selected_year:
        filtered_df = filtered_df[filtered_df['Year'].isin(selected_year)]
    if selected_type:
        filtered_df = filtered_df[filtered_df['Type'].isin(selected_type)]

    # 6. RESULTS
    st.markdown(f"<p style='text-align: center; font-size: 0.85rem; color: #80868B !important;'>Showing {len(filtered_df)} lectures</p>", unsafe_allow_html=True)
    st.markdown("<hr style='margin-top: 0;'>", unsafe_allow_html=True)

    for i, row in filtered_df.iterrows():
        source_url = str(row['Source Link'])
        file_id = ""
        if 'id=' in source_url:
            file_id = source_url.split('id=')[-1].split('&')[0]
        elif 'file/d/' in source_url:
            file_id = source_url.split('file/d/')[-1].split('/')[0]

        # Use the official Google preview link for the most stable external playback
        preview_url = f"https://drive.google.com/file/d/{file_id}/view"

        # HTML Structure for the Card
        st.markdown(f"""
            <div class="lecture-card">
                <div class="card-title">{row['Code']}</div>
                <div>
                    <span class="badge">🌍 {row['Language']}</span>
                    <span class="badge">🏷️ {row['Type']}</span>
                </div>
                <div class="meta-text">📍 {row['Location']}  •  📅 {row['Date']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Audio Player (Native)
        # Using export=download often tricks browsers into playing it directly better than export=open
        audio_stream = f"https://drive.google.com/uc?export=download&id={file_id}"
        st.audio(audio_stream, format="audio/mp3")

        # Clean Action Buttons under the audio player
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col1:
            st.link_button("▶️ Web Player", preview_url, use_container_width=True)
        with btn_col2:
            st.link_button("📥 Download", source_url, use_container_width=True)
        with btn_col3:
            share_text = f"Listen to Maharaj: {row['Code']} - {preview_url}"
            st.link_button("🔗 Share", f"https://wa.me/?text={share_text}", use_container_width=True)
        
        st.write("") # Spacer between cards

else:
    st.error("Could not load lecture data. Please check the CSV file.")
