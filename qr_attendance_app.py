import streamlit as st
import pandas as pd
from datetime import datetime
import cv2
import os

st.set_page_config(page_title="QR Attendance Scanner", layout="centered")
st.title("📷 QR Code Scanner for Student Attendance")

# Load or create CSV
csv_file = "attendance_log.csv"
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=["Name", "Roll Number", "Semester", "Class", "Batch", "Timestamp"])

# Button to start scanning
if st.button("Start Scanning"):
    st.info("Press 'q' in the scanner window to stop scanning.")

    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to access webcam.")
            break

        data, bbox, _ = detector.detectAndDecode(frame)
        if bbox is not None and data:
            try:
                parts = dict(part.strip().split(": ", 1) for part in data.split(", "))
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                row = {
                    "Name": parts.get("Name", ""),
                    "Roll Number": parts.get("Roll", ""),
                    "Semester": parts.get("Semester", ""),
                    "Class": parts.get("Class", ""),
                    "Batch": parts.get("Batch", ""),
                    "Timestamp": timestamp
                }

                if not ((df["Roll Number"] == row["Roll Number"]) & (df["Timestamp"] == row["Timestamp"])).any():
                    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
                    df.to_csv(csv_file, index=False)
                    st.success(f"✅ Scanned: {row['Name']} ({row['Roll Number']}) at {timestamp}")
            except Exception as e:
                st.warning(f"Could not parse QR data: {e}")

        cv2.imshow("Scan QR - Press q to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Show current log
st.subheader("📄 Attendance Log")
st.dataframe(df)
