import streamlit as st

def contact_form():
    with st.form("Emergency Contacts"):
        name = st.text_input("First Name")
        relation = st.text_input("Your Relation to User")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        submit_button =  st.form_submit_button("Submit")

        if submit_button:
            if name and relation and phone:
                # Checks if the contact was already added.
                if "contacts" not in st.session_state:
                    st.session_state.contacts = []

                # Adds new contact to session state if not added before
                st.session_state.contacts.append({
                    "Name": name,
                    "Relation": relation,
                    "Phone": phone,
                    "Email": email
                    #"Delete": False  # Column for deletion checkbox in the table
                })

                st.success("Contact added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all required fields.")
