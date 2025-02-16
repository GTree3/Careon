import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Hide the Streamlit anchor link using CSS
st.markdown("""
    <style>
        h1 { text-align: center; }
        .stMarkdown a { display: none !important; }  /* Hides the link */
    </style>
    <h1>Fall Detection AI</h1>
""", unsafe_allow_html=True)

# Initialize the camera
cap = cv2.VideoCapture(0)

# --- Create Columns for Centering Buttons ---
col1, col2, col3 = st.columns([1, 2, 1])  # Middle column is wider to center the buttons

with col2:  # Center column
    start_button_pressed = st.button("Start Camera", use_container_width=True)
    stop_button_pressed = st.button("Stop Camera", use_container_width=True)

# Placeholder for displaying video and fall alerts
frame_placeholder = st.empty()
alert_placeholder = st.empty()

# Creates a session state to store the previous frame’s average shoulder height, but starts at none, since the camera just started
if "prev_avg_shoulder_y" not in st.session_state:
    st.session_state["prev_avg_shoulder_y"] = None

# Creates a session state to store the time of the last fall
if "last_time" not in st.session_state:
    st.session_state["last_time"] = time.time()

# Creates a session state to store the number of frames that passed
if "frame_count" not in st.session_state:
    st.session_state["frame_count"] = 0

# Fall detection function - inspired by https://github.com/barkhaaroraa/fall_detection_DL
def fallDetection(landmarks, h, prev_avg_shoulder_y):
    l_shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * h
    r_shoulder_y = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * h

    avg_shoulder_y = (l_shoulder_y + r_shoulder_y) / 2

    # Fall is not detected if there was no previous saved height to reference to
    if prev_avg_shoulder_y is None:
        return False, avg_shoulder_y

    # Gradual height update to prevent extreme jumps
    prev_avg_shoulder_y = (prev_avg_shoulder_y * 0.8) + (avg_shoulder_y * 0.2)

    # Sensitivity threshold for fall detection - if the height increases by 30%, fall detection will be triggered
    fall_threshold = prev_avg_shoulder_y * 1.3

    # Check if the average shoulder height suddenly drops below the threshold, then  fall detected (returns true)
    if avg_shoulder_y > fall_threshold:
        return True, prev_avg_shoulder_y
    else:
        return False, prev_avg_shoulder_y

# Pose detection - 0.5 to ensure a balanced confidence. Too much will cause less falls caught
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

    # This loop continuously captures frames while the camera is open and the user wants to record.
    while cap.isOpened() and start_button_pressed and not stop_button_pressed:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture frame!")
            break

        # Convert frame to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Pose
        results = pose.process(image)

        # Detects human, extracts pose landmarks and gets the frame height 
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            landmarks = results.pose_landmarks.landmark 
            h, _, _ = frame.shape
            
            st.session_state["frame_count"] += 1

            # Wait for 10 frames before detecting falls to have a baseline to compare falls to + time check to prevent overload of fall detection at every frame
            if st.session_state["frame_count"] > 10:
                curr_time = time.time()
                if curr_time - st.session_state["last_time"] > 1:
                    fall_detected, st.session_state["prev_avg_shoulder_y"] = fallDetection(
                        landmarks, h, st.session_state["prev_avg_shoulder_y"]
                    )

                    if fall_detected:
                        alert_placeholder.error("⚠️ Fall Detected!")
                    else:
                        alert_placeholder.success("✅ Person is standing safely.")

                    # Update last checked time
                    st.session_state["last_time"] = curr_time

        # Display the current frame
        frame_placeholder.image(image, channels="RGB", use_container_width=True)

        if cv2.waitKey(1) & stop_button_pressed:
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
