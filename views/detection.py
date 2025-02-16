import streamlit as st
import cv2
import numpy as np
import tempfile

st.title("Fall Detection AI")

# Initialize the camera (index 0 means the first available camera)
cap = cv2.VideoCapture(0)

# Start button
start_button_pressed = st.button("Start Camera")

# Stop button
stop_button_pressed = st.button("Stop Camera")

# Placeholder frame for displaying the video frames
frame_placeholder = st.empty() # Read a frame from the camera

# Loop to continuously capture frames while the camera is active
while cap.isOpened() and start_button_pressed and not stop_button_pressed:
    ret, frame = cap.read()

    if not ret:
        st.write("Unable to capture frames. The video capture has ended.")
        break
    
    # Convert the frame from BGR (OpenCV default) to RGB (for Streamlit display)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the current frame in the Streamlit app
    frame_placeholder.image(frame, channels="RGB")

    if cv2.waitKey(1) & stop_button_pressed: # Stops the camera from capturing
        break

# Release the camera resource (important to free up hardware access)
cap.release()

# Closes all OpenCV windows (though Streamlit doesn't open them explicitly)
cv2.destroyAllWindows()
