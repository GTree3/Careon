import streamlit as st

# Hide the Streamlit anchor link using CSS
st.markdown("""
    <style>
        h1 { text-align: center; }
        .stMarkdown a { display: none !important; }
    </style>
    <h1>About Us</h1>
""", unsafe_allow_html=True)

st.image("./assets/Careon - Logo.png", use_container_width=True)

st.markdown("""
    <style>
        p { text-align: center; }
        .stMarkdown a { display: none !important; }
    </style>
    <p>
       Careon is an innovative AI-powered web application aimed at enhancing the safety and 
       independence of elderly individuals. By leveraging motion detection and intelligent 
       alert systems, Careon continuously monitors seniors for unusual inactivity or potential 
       falls and notifies designated contacts or emergency services if necessary. The platform 
       includes integrated two-way communication, allowing seniors to easily connect with family 
       members or caregivers. Additionally, Careon offers hazard prevention by identifying 
       environmental risks in the home that could lead to falls. With a focus on accessibility, 
       user-friendliness, and seamless integration, Careon provides a reliable, automated safety 
       net that empowers elderly individuals while offering peace of mind to their loved ones.</p>
""", unsafe_allow_html=True)



