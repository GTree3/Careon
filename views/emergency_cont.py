import streamlit as st
import pandas as pd

st.markdown("""
    <style>
        h1 { text-align: center; }
        h1 a { display: none !important; }   /* Hide only the Streamlit auto-generated header links */
    </style>
    <h1>Emergency Contacts</h1>
""", unsafe_allow_html=True)

from forms.contact import *

@st.dialog("Enter your emergency contact")
def show_contact_form():
    contact_form()

# --- Create Columns for Centering Buttons ---
col1, col2, col3 = st.columns([1, 2, 1])  # Middle column is wider to center the buttons

with col2:  # Center column
    if st.button ("Please Enter Emergency Contact(s)👆", use_container_width=True):
        show_contact_form()

# --- Display contacts as a table
st.markdown("""
    <h3 style='text-align: center; margin-top: 30px; margin-bottom: 5px;'>
        Saved Emergency Contacts
    </h3>
""", unsafe_allow_html=True)

if "contacts" in st.session_state and st.session_state.contacts:
    st.markdown("""
    <style>
        .stMarkdown p { margin-bottom: 5px !important; }
        div[data-testid="stColumns"] { margin-top: -15px !important; }
    </style>
""", unsafe_allow_html=True)

    # Display table headers
    headers = ["Name", "Relation", "Phone", "Email", "Delete Contact"]
    cols = st.columns(5)

    for col, header in zip(cols, headers):
     col.markdown(f"<p style='text-align: center; font-weight: bold;'>{header}</p>", unsafe_allow_html=True)

    # Display contacts
    for contact in st.session_state.contacts:
        cols = st.columns(5, gap="small", border=True)
        
        cols[0].markdown(f"<p style='text-align: center;'>{contact['Name']}</p>", unsafe_allow_html=True)
        cols[1].markdown(f"<p style='text-align: center;'>{contact['Relation']}</p>", unsafe_allow_html=True)
        cols[2].markdown(f"<p style='text-align: center;'>{contact['Phone']}</p>", unsafe_allow_html=True)
        cols[3].markdown(f"<p style='text-align: center;'><a href='mailto:{contact['Email']}'>{contact['Email']}</a></p>", unsafe_allow_html=True)

        if cols[4].button("Delete", key=contact["Cont_id"], use_container_width=True):
             delete_contact(contact["Cont_id"])
             st.rerun()
else:
    st.info("No emergency contacts added yet.")




    