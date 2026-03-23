import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import random
import string

# Page Configuration
st.set_page_config(page_title="CPDOHO eTAG", layout="wide", page_icon="🏥")

# --- UPDATED HIGH-CONTRAST CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f1f8f6 !important; }

    /* 1. FORCE DARK TEXT ON ALL MAIN CONTENT */
    [data-testid="stMain"] *, .stMarkdown p, .stText, .stCaption, label p, span, h4 {
        color: #1a1a1a !important; 
    }

    /* 2. FORCED VISIBILITY FOR INPUT TEXT */
    /* This ensures what you TYPE is black and visible */
    input, textarea, [data-baseweb="select"] span, [data-baseweb="select"] div {
        color: #000000 !important; 
        -webkit-text-fill-color: #000000 !important;
    }

    /* 3. BORDERLESS UNDERLINED STYLE */
    input, textarea, [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: none !important; 
        border-bottom: 2px solid #1b4d3e !important; 
        border-radius: 0px !important;
        box-shadow: none !important;
    }

    input:focus, textarea:focus {
        border-bottom: 2px solid #efb519 !important;
        outline: none !important;
    }

    /* 4. NAVIGATION STATUS */
    .nav-status {
        background-color: #0038a8; color: #ffffff !important;
        padding: 8px 15px; border-radius: 4px; border-left: 8px solid #efb519;
        margin-bottom: 15px; font-weight: bold; font-size: 0.95rem;
    }
    .nav-status span { color: #ffffff !important; }

    /* 5. SIDEBAR STYLE */
    [data-testid="stSidebar"] { background-color: #1b4d3e !important; border-right: 5px solid #efb519 !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }

    /* 6. BUTTON THEMING */
    div[data-testid="stForm"] button[kind="primaryFormSubmit"] {
        background-color: #1b4d3e !important; color: #ffffff !important;
        border: none !important; font-weight: bold !important;
    }
    .stLinkButton > a {
        background-color: #efb519 !important; color: #0038a8 !important;
        font-weight: bold !important; border: none !important;
    }

    .footer { text-align: center; padding: 20px; color: #1b4d3e !important; border-top: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# --- GOOGLE SHEETS LOGIC ---
def get_gspread_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    return gspread.authorize(creds)

@st.cache_data(ttl=60)
def get_data():
    try:
        client = get_gspread_client()
        sheet_id = "1kJCOUc-bObq7Ogp9xk-6u48HE3MbkogdcQ5oC3G5mW8"
        sheet = client.open_by_key(sheet_id).worksheet("rawdataV2")
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        if not df.empty:
            df['CATEGORY'] = df['CATEGORY'].astype(str).str.strip()
            df['CATEGORY'] = df['CATEGORY'].replace('BAGUIO HRH', 'HRH SECTION')
            df = df[df['CATEGORY'] != ""].dropna(subset=['CATEGORY'])
        return df
    except:
        return pd.DataFrame()

df = get_data()

# --- SIDEBAR WITH SIDE-BY-SIDE LOGOS ---
with st.sidebar:
    # Use columns to put logos in the same row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/3/33/Department_of_Health_%28DOH%29_PHL.svg", width=70)
    with col2:
        # Note: This requires the file to be in your directory
        try:
            st.image("DOH-CHD-CAR.png", width=70)
        except:
            st.write("DOH-CAR")
    with col3:
        st.image("https://upload.wikimedia.org/wikipedia/commons/c/ce/Bagong_Pilipinas_Logo.svg", width=70)
    
    st.markdown("### **DOH - CHD CAR**")
    st.markdown("---")
    
    if "show_form" not in st.session_state: st.session_state.show_form = False
    
    if st.button("➕ ADD NEW RESOURCE", use_container_width=True):
        st.session_state.show_form = True

    st.markdown("---")
    selected_category = "All Resources" # Default if df is empty
    if not df.empty:
        categories_list = sorted(df['CATEGORY'].unique().tolist())
        selected_category = st.radio("SELECT SECTION:", ["All Resources"] + categories_list)

    # 4. EXTERNAL LINKS SECTION
    st.markdown("---")
    st.markdown("### **🌐 QUICK LINKS**")
    st.link_button("📘 FACEBOOK PAGE", "https://www.facebook.com/dohchdcar", use_container_width=True)
    st.link_button("🏛️ OFFICIAL WEBSITE", "https://caro.doh.gov.ph/", use_container_width=True)
    st.link_button("📧 WEBMAIL", "https://mail.doh.gov.ph", use_container_width=True)         

# --- MAIN HEADER ---
st.markdown(f"""
    <div style="background-color: #ffffff; padding: 15px; border-radius: 10px; border-bottom: 5px solid #efb519; margin-bottom: 15px;">
        <p style="color: #0038a8; margin: 0; font-size: 1.8rem; font-weight: 800;">CPDOHO eTAG</p>
        <p style="color: #1b4d3e; margin: 0; font-size: 1.1rem;">Electronic Tracking Assistance Guide</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""<div class="nav-status">📍 VIEWING: <span>{selected_category.upper()}</span></div>""", unsafe_allow_html=True)

# --- NEW ENTRY FORM ---
if st.session_state.show_form:
    st.markdown('<p style="color:#1b4d3e; font-weight:bold; font-size:1.2rem;">📝 New Resource Entry</p>', unsafe_allow_html=True)
    
    with st.form("entry_form", clear_on_submit=True):
        rand_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        gen_id = f"TAG-{datetime.now().strftime('%y%m%d')}-{rand_id}"
        st.caption(f"ID: {gen_id}")
        
        c1, c2, c3 = st.columns([2,2,1])
        with c1: t_title = st.text_input("Title")
        with c2: t_url = st.text_input("URL")
        with c3: 
            # Check if df is empty to avoid errors in selectbox
            cat_list = sorted(list(set(df['CATEGORY'].tolist() + ["HRH SECTION"]))) if not df.empty else ["HRH SECTION"]
            t_cat = st.selectbox("Section", cat_list)
        
        t_desc = st.text_input("Short Description")
        
        if st.form_submit_button("SAVE TO DATABASE"):
            if t_title and t_url:
                client = get_gspread_client()
                # Ensure the sheet name 'stremlit' matches your setup
                t_sheet = client.open_by_key("1kJCOUc-bObq7Ogp9xk-6u48HE3MbkogdcQ5oC3G5mW8").worksheet("stremlit")
                t_sheet.append_row([gen_id, t_title, t_desc, t_url, t_cat])
                st.success("Saved!")
                st.session_state.show_form = False
                st.cache_data.clear()
                st.rerun()

    if st.button("✖ CANCEL"):
        st.session_state.show_form = False
        st.rerun()
    st.markdown("---")

# --- LISTING ---
if not df.empty:
    search = st.text_input("🔍 Quick Search", placeholder="Filter resources...")
    
    f_df = df.copy()
    if selected_category != "All Resources":
        f_df = f_df[f_df['CATEGORY'] == selected_category]
    if search:
        f_df = f_df[f_df['TITLE'].str.contains(search, case=False, na=False)]

    for _, row in f_df.iterrows():
        col_content, col_btn = st.columns([6, 1])
        with col_content:
            st.markdown(f"""
                <p style="color: #8b0000; font-weight: bold; font-size: 1rem; margin: 0;">{row['TITLE']}</p>
                <p style="color: #444; font-size: 0.85rem; margin: 0;">{row['DESCRIPTION'] or 'N/A'}</p>
                <p style="color: #777; font-size: 0.75rem; font-style: italic;">ID: {row.get('RECID', 'N/A')} | {row['CATEGORY']}</p>
            """, unsafe_allow_html=True)
        with col_btn:
            st.link_button("OPEN", row['LINK'], use_container_width=True)
        st.markdown("<div style='border-bottom:1px solid #eee; margin: 5px 0;'></div>", unsafe_allow_html=True)

# --- DYNAMIC FOOTER ---
current_year = datetime.now().year
st.markdown(f"""
    <div class="footer">
        © {current_year} CPDOHO - Baguio/Benguet MiniSystem ver1
    </div>
    """, unsafe_allow_html=True)