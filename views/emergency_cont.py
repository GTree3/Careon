import streamlit as st
import pandas as pd

st.title("Emergency Contacts")

from forms.contact import contact_form

@st.dialog("Enter your emergency contact")
def show_contact_form():
    contact_form()

if st.button ("Please Enter Emergency Contact(s)👆"):
        show_contact_form()

# --- Display contacts as a table
st.subheader("Saved Emergency Contacts")

if "contacts" in st.session_state and st.session_state.contacts:
    st.dataframe(st.session_state.contacts, use_container_width=True)  # Display contacts as a table
else:
    st.info("No emergency contacts added yet.")




    