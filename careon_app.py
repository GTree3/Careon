import streamlit as st

#--- PAGE SETUP ---
about_page = st.Page(
    page="views/about_us.py",
    title="About Us",
    icon=":material/group:",
    default=True,
)
project_1_page = st.Page(
    page="views/detection.py",
    title="Fall Detection AI",
    icon=":material/radar:",
)
project_2_page = st.Page(
    page="views/emergency_cont.py",
    title="Emergency Contacts",
    icon=":material/call:",
)
project_3_page = st.Page(
    page="views/chatbot.py",
    title="Memory Chat Bot",
    icon=":material/smart_toy:",
)

# --- NAVIGATION SETUP (WITH SECTIONS) ---
pg = st.navigation(
    {
        "Info": [about_page],
        "Functions": [project_1_page, project_2_page, project_3_page],
    }
)

# --- SHARED ON ALL PAGES ---
st.logo("assets/Careon_Logo.png")
st.sidebar.text("Made with ❤️ by CTRL+ALT+DEFEAT")
# --- RUN NAVIGATION ---
pg.run()