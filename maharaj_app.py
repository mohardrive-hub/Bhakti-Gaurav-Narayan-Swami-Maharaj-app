import streamlit as st
import pandas as pd

# 1. Config
st.set_page_config(page_title="Maharaj App", page_icon="🙏", layout="centered")

# 2. Modern "App" CSS
st.markdown("""
    <style>
    /* Global Styles */
    .stApp { background-color: #FAFAFA; }
    h2 { color: #D84315; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Search Bar Styling */
    .stTextInput>div>div>input {
        border-radius: 25px;
        border: 1px solid #FFCCBC;
        padding: 10px 20px;
    }

    /* Modern Lecture Card */
    .lecture-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        transition: transform 0.2s;
    }
    .lecture-card:active { transform: scale(0.98); }
    
    .category-pill {
        background: #FFF3E0;
        color: #E65100;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: bold;
        text-transform: uppercase;
    }

    .play-btn {
        background-color: #E65100 !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("Maharaj_Perfect_Metadata.csv")

df = load_data()

# --- APP HEADER ---
st.markdown("<div style='text-align: center; padding-top: 20px;'>", unsafe_allow_html=True)
st.image("https://cdn-icons-png.flaticon.com/512/2903/2903513.png", width=60)
st.markdown("<h2>Gaurav Narayan Maharaj</h2>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- AI & SEARCH SECTION ---
tabs = st.tabs(["🔍 Search", "🤖 AI Librarian", "📌 Categories"])

with tabs[0]:
    search_query = st.text_input("", placeholder="Find a lecture, verse, or place...", key="main_search")

with tabs[1]:
    st.info("Ask me anything about Maharaj's lectures (Coming Soon with Gemini API)")
    ai_prompt = st.text_input("Ask AI", placeholder="e.g. Which lectures are about Krishna's pastimes in Vrindavan?")

with tabs[2]:
    st.write("Browse by Content Type")
    cols = st.columns(3)
    types = list(df['Type'].unique())
    for i, t in enumerate(types[:6]):
        cols[i % 3].button(t, use_container_width=True)

# --- LISTING ---
filtered_df = df.copy()
if search_query:
    filtered_df = df[df['Code'].str.contains(search_query, case=False, na=False) | 
                     df['Location'].str.contains(search_query, case=False, na=False)]

st.markdown(f"<p style='color: gray; font-size: 0.8rem;'>{len(filtered_df)} Lectures Found</p>", unsafe_allow_html=True)

for i, row in filtered_df.iterrows():
    file_id = row['Source Link'].split('id=')[-1].split('&')[0]
    preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
    
    with st.container():
        st.markdown(f"""
            <div class="lecture-card">
                <span class="category-pill">{row['Type']}</span>
                <div style="font-size: 1.1rem; font-weight: 700; margin-top: 10px; color: #333;">{row['Code']}</div>
                <div style="color: #888; font-size: 0.85rem; margin-bottom: 15px;">
                    📅 {row['Date']} • 📍 {row['Location']} • 🗣️ {row['Language']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.link_button("▶️ LISTEN NOW", preview_url, use_container_width=True)
        with c2:
            st.link_button("📥 DOWNLOAD", row['Source Link'], use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
