import streamlit as st
import pandas as pd
from datetime import datetime
import cv2
from pyzbar.pyzbar import decode
import tempfile
import os

st.title("📷 QR Code Scanner for Student Attendance")

# Load or create CSV
csv_file = "attendance_log.csv"
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=["Name", "Roll Number", "Semester", "Class", "Batch", "Timestamp"])

# Button to start scanning
if st.button("Start Scanning"):
    st.info("Press 'q' to stop scanning.")
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        for code in decode(frame):
            qr_data = code.data.decode('utf-8')
            parts = dict(part.strip().split(": ", 1) for part in qr_data.split(", "))
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            row = {
                "Name": parts.get("Name", ""),
                "Roll Number": parts.get("Roll", ""),
                "Semester": parts.get("Semester", ""),
                "Class": parts.get("Class", ""),
                "Batch": parts.get("Batch", ""),
                "Timestamp": timestamp
            }

            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
            st.success(f"Scanned: {row['Name']} ({row['Roll Number']})")
            df.to_csv(csv_file, index=False)

        cv2.imshow("Scan QR - Press q to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

st.subheader("📄 Attendance Log")
st.dataframe(df)
