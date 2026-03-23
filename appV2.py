import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import random
import string

# Page Configuration
st.set_page_config(page_title="CPDOHO eTAG", layout="wide", page_icon="🏥")

# --- THEMED CSS: FORCED GOLD & SMOOTH ANIMATION ---
st.markdown("""
    <style>
    /* 1. FORCE SMOOTH SCROLLING VIA CSS ANIMATION */
    html, body, [data-testid="stAppViewContainer"] {
        scroll-behavior: smooth !important;
    }

    /* 2. MAIN BACKGROUND */
    .stApp { background-color: #f1f8f6 !important; }

    /* 3. GLOBAL TEXT VISIBILITY */
    [data-testid="stMain"] *, .stMarkdown p, .stText, .stCaption, label p, span, h4 {
        color: #1a1a1a !important; 
    }

    /* 4. INPUT BOXES: WHITE BG + BLACK TEXT */
    input, textarea, [data-baseweb="select"] span, [data-baseweb="select"] div {
        color: #000000 !important; 
        -webkit-text-fill-color: #000000 !important;
    }
    input, textarea, [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: none !important; 
        border-bottom: 2px solid #1b4d3e !important; 
        border-radius: 0px !important;
    }

    /* 5. SIDEBAR */
    [data-testid="stSidebar"] { background-color: #1b4d3e !important; border-right: 5px solid #efb519 !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    
    /* 6. BUTTONS: FORCED DOH GOLD (#efb519) */
    /* Targeting Form Submit Buttons */
    div[data-testid="stForm"] button[kind="primaryFormSubmit"], 
    div[data-testid="stForm"] button[kind="secondaryFormSubmit"] {
        background-color: #efb519 !important; 
        color: #1b4d3e !important;
        border: 2px solid #1b4d3e !important;
        font-weight: bold !important;
    }

    /* Targeting "Open" Link Buttons */
    .stLinkButton > a {
        background-color: #efb519 !important; 
        color: #0038a8 !important;
        font-weight: 800 !important;
        border: 1px solid #1b4d3e !important;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1) !important;
    }

    /* 7. FLOATING SCROLL BUTTON: DOH GOLD */
    .scroll-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 9999;
        background-color: #efb519 !important;
        color: #1b4d3e !important;
        border: 3px solid #1b4d3e;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        text-decoration: none !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        font-weight: bold;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
        transition: transform 0.2s ease;
    }
    .scroll-btn:hover {
        transform: scale(1.1);
        background-color: #1b4d3e !important;
        color: #efb519 !important;
    }

    .footer { text-align: center; padding: 20px; color: #1b4d3e !important; border-top: 1px solid #ddd; }
    </style>
    
    <div id="top-anchor"></div>
    <a href="#top-anchor" class="scroll-btn" title="Back to Top">▲</a>
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

# --- SIDEBAR ---
with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1: st.image("https://upload.wikimedia.org/wikipedia/commons/3/33/Department_of_Health_%28DOH%29_PHL.svg", width=70)
    with col2:
        try: st.image("DOH-CHD-CAR.png", width=70)
        except: st.write("DOH-CAR")
    with col3: st.image("https://upload.wikimedia.org/wikipedia/commons/c/ce/Bagong_Pilipinas_Logo.svg", width=70)
    
    st.markdown("### **DOH - CHD CAR**")
    st.markdown("---")
    
    if "show_form" not in st.session_state: st.session_state.show_form = False
    
    if st.button("➕ ADD NEW RESOURCE", use_container_width=True):
        st.session_state.show_form = True

    st.markdown("---")
    selected_category = "All Resources" 
    if not df.empty:
        categories_list = sorted(df['CATEGORY'].unique().tolist())
        selected_category = st.radio("SELECT SECTION:", ["All Resources"] + categories_list)

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

st.markdown(f"""<div style="background-color: #0038a8; color: #ffffff; padding: 8px 15px; border-radius: 4px; border-left: 8px solid #efb519; margin-bottom: 15px; font-weight: bold;">📍 VIEWING: {selected_category.upper()}</div>""", unsafe_allow_html=True)

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
            cat_list = sorted(list(set(df['CATEGORY'].tolist() + ["HRH SECTION"]))) if not df.empty else ["HRH SECTION"]
            t_cat = st.selectbox("Section", cat_list)
        
        t_desc = st.text_input("Short Description")
        
        if st.form_submit_button("SAVE TO DATABASE"):
            if t_title and t_url:
                client = get_gspread_client()
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
st.markdown(f"""<div class="footer">© {current_year} CPDOHO - Baguio/Benguet MiniSystem ver1</div>""", unsafe_allow_html=True)