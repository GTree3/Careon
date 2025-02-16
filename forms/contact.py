import streamlit as st
import uuid

# Generates Streamlit form for adding contacts
def contact_form():
    with st.form("Emergency Contacts"):
        name = st.text_input("First Name")
        relation = st.text_input("Your Relation to User")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        submit_button =  st.form_submit_button("Submit")

        if submit_button:
            if name and relation and phone:
                # Checks if "contacts" key exists in the st.session_state dictionary
                if "contacts" not in st.session_state:
                    # Initialises "contacts" key with an empty list
                    st.session_state.contacts = []

                # Adds new contact to session state if not added before
                st.session_state.contacts.append({
                    "Cont_id": str(uuid.uuid4()),  # Generates a unique ID for each contact
                    "Name": name,
                    "Relation": relation,
                    "Phone": phone,
                    "Email": email
                })

                st.success("Contact added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all required fields.")

# Delete contacts given an id
def delete_contact(cont_id: str):
    # Check if this contact exists
    cont = next(item for item in st.session_state.contacts if item["Cont_id"] == cont_id)
    if cont:
        # Delete contacts
        st.session_state.contacts.remove(cont)
    else:
        # Display warning
        st.warning('This contact does not exist', icon="⚠️")
