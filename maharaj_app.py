import streamlit as st
import pandas as pd

# 1. Page Config with Mobile-friendly Sidebar
st.set_page_config(page_title="Maharaj Lectures", page_icon="🕉️", layout="wide")

# 2. Advanced Custom CSS for "App Look"
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #FFF9F2; }
    
    /* Card Styling */
    .lecture-card {
        background: white;
        padding: 18px;
        border-radius: 15px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #FFE0B2;
    }
    
    /* Title Styling */
    .lecture-title {
        color: #BF360C !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 5px;
    }
    
    /* Metadata Pills */
    .pill {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 5px;
        background: #FBE9E7;
        color: #D84315;
    }
    
    /* Custom Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFF3E0;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("Maharaj_Perfect_Metadata.csv")

df = load_data()

# --- HEADER ---
st.markdown("<h2 style='text-align: center; color: #E65100;'>🙏 Bhakti Gaurav Narayan Swami</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #5D4037;'>Audio Lecture Library</p>", unsafe_allow_html=True)

# --- SIDEBAR FILTERS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2903/2903513.png", width=80)
search_query = st.sidebar.text_input("🔍 Search", placeholder="Topic, Place, Verse...")

with st.sidebar.expander("🛠️ Advanced Filters"):
    selected_lang = st.multiselect("Language", df['Language'].unique(), default=df['Language'].unique())
    selected_year = st.multiselect("Year", sorted(df['Year'].unique(), reverse=True))
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
st.write(f"Showing {len(filtered_df)} lectures")

for i, row in filtered_df.iterrows():
    file_id = row['Source Link'].split('id=')[-1].split('&')[0]
    preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
    
    with st.container():
        st.markdown(f"""
            <div class="lecture-card">
                <div class="lecture-title">{row['Code']}</div>
                <div style="margin: 8px 0;">
                    <span class="pill">🌍 {row['Language']}</span>
                    <span class="pill">📍 {row['Location']}</span>
                    <span class="pill">📅 {row['Year']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Action Buttons
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.link_button("▶️ Listen Now", preview_url, use_container_width=True)
        with col2:
            st.link_button("📥 Save", row['Source Link'], use_container_width=True)
        with col3:
            # WhatsApp Share Link
            share_text = f"Listen to Maharaj: {row['Code']} - {preview_url}"
            st.link_button("🔗 Share", f"https://wa.me/?text={share_text}", use_container_width=True)
        st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)
