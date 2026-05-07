import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Maharaj Audio", page_icon="🕉️", layout="centered")

# 2. Safe CSS strictly for the Cards (No messing with Streamlit's native text)
st.markdown("""
    <style>
    /* Hide Streamlit Clutter */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Beautiful Lecture Card */
    .maharaj-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border-left: 5px solid #D84315; /* Saffron Accent */
    }
    
    .maharaj-title {
        color: #D84315;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 10px;
        line-height: 1.3;
    }

    .maharaj-tag {
        display: inline-block;
        background-color: #FFF3E0;
        color: #E65100;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    .maharaj-meta {
        color: #555555;
        font-size: 0.85rem;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Load Data
@st.cache_data
def load_data():
    try:
        return pd.read_csv("Maharaj_Perfect_Metadata.csv")
    except:
        return pd.DataFrame()

df = load_data()

# 4. App Header
st.image("https://cdn-icons-png.flaticon.com/512/2903/2903513.png", width=60)
st.title("Maharaj Audio Library")
st.caption("Official Archive of HH Bhakti Gaurav Narayan Swami")

if not df.empty:
    # 5. Search & Filters (Now perfectly readable thanks to config.toml)
    search_query = st.text_input("🔍 Search", placeholder="Find a topic, place, or verse...")
    
    with st.expander("⚙️ Advanced Filters"):
        col1, col2 = st.columns(2)
        with col1:
            selected_lang = st.multiselect("Language", df['Language'].unique())
        with col2:
            selected_type = st.multiselect("Category", df['Type'].unique())
            
        years = sorted([y for y in df['Year'].unique() if pd.notna(y)], reverse=True)
        selected_year = st.multiselect("Year", years)

    # Filtering Logic
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

    st.write(f"**{len(filtered_df)} lectures found**")
    st.divider()

    # 6. Render Lecture Cards
    for i, row in filtered_df.iterrows():
        source_url = str(row['Source Link'])
        file_id = ""
        if 'id=' in source_url:
            file_id = source_url.split('id=')[-1].split('&')[0]
        elif 'file/d/' in source_url:
            file_id = source_url.split('file/d/')[-1].split('/')[0]

        preview_url = f"https://drive.google.com/file/d/{file_id}/view"
        audio_stream = f"https://drive.google.com/uc?export=download&id={file_id}"

        # Draw the custom HTML card
        st.markdown(f"""
            <div class="maharaj-card">
                <div class="maharaj-title">{row['Code']}</div>
                <div>
                    <span class="maharaj-tag">🌍 {row['Language']}</span>
                    <span class="maharaj-tag">🏷️ {row['Type']}</span>
                </div>
                <div class="maharaj-meta">📍 {row['Location']}  •  📅 {row['Date']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Audio Player
        st.audio(audio_stream, format="audio/mp3")

        # Clean Native Buttons
        c1, c2, c3 = st.columns(3)
        with c1:
            st.link_button("▶️ Web Player", preview_url, use_container_width=True)
        with c2:
            st.link_button("📥 Download", source_url, use_container_width=True)
        with c3:
            share_text = f"Listen to Maharaj: {row['Code']} - {preview_url}"
            st.link_button("🔗 Share", f"https://wa.me/?text={share_text}", use_container_width=True)
        
        st.write("") # Small spacer
else:
    st.error("Data not found. Please check your CSV.")
