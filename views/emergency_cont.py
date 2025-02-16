import streamlit as st
import pandas as pd

st.title("Emergency Contacts")

from forms.contact import *

@st.dialog("Enter your emergency contact")
def show_contact_form():
    contact_form()

if st.button ("Please Enter Emergency Contact(s)👆"):
        show_contact_form()

# --- Display contacts as a table
st.subheader("Saved Emergency Contacts")

if "contacts" in st.session_state and st.session_state.contacts:
    # Display table headers
    headers = ["Name", "Relation", "Phone", "Email", "Delete Contact"]
    cols = st.columns(5)
    for col, header in zip(cols, headers):
         col.write(f"**{header}**")
    # Display contacts
    for contact in st.session_state.contacts:
        cols = st.columns(5, border=True)
        cols[0].write(contact["Name"])
        cols[1].write(contact["Relation"])
        cols[2].write(contact["Phone"])
        cols[3].write(contact["Email"])
        if cols[4].button("Delete", key=contact["Cont_id"]):
             delete_contact(contact["Cont_id"])
             st.rerun()
else:
    st.info("No emergency contacts added yet.")




    