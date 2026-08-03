import streamlit as st

st.set_page_config(
    page_title="Receipt Information Extractor",
    page_icon="🧾",
    layout="wide"
)

st.markdown(
    """
    <div style="
        background: linear-gradient(90deg,#2563EB,#06B6D4);
        padding:20px;
        border-radius:12px;
        color:white;
        margin-bottom:20px;
    ">

    <h1 style="margin-bottom:0;">
        🧾 Smart Receipt Manager
    </h1>

    <p style="margin-top:5px;font-size:18px;">
        AI-powered OCR & Expense Management System
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

page = st.radio(
    "Navigation",
    [
        "🧾 Extractor",
        "📜 History",
        "📊 Dashboard",
        "⚙ Settings"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()

if page == "🧾 Extractor":
    from ui.extractor_page import extractor_page
    extractor_page()

elif page == "📜 History":
    from ui.history_page import history_page
    history_page()

elif page == "📊 Dashboard":
    from ui.dashboard_page import dashboard_page
    dashboard_page()

else:
    from ui.settings_page import settings_page
    settings_page()