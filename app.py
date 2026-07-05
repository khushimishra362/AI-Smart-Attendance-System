# IMPORTING LIBRARIES
import os
import pickle
import shutil
import subprocess
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from Database import *
from save_encodings import save_all_encodings
from student_registation import capture_student_images

#STREAMLIT CONFIGURATION
create_database()

st.set_page_config(
    page_title="Smart AI Attendance System",
    page_icon="🎓",
    layout="wide"
)

#REGISTATION DIALOG
@st.dialog("📸 Registration Instructions")
def registration_dialog(student_name):

    st.markdown("""
### Please follow these instructions

✅ Stand in front of the camera.

✅ Keep your face clearly visible.

✅ Stay still.

✅ Slowly move your face naturally.

✅ Wait until registration completes.
""")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("✅ Start Capturing"):

            message = capture_student_images(student_name)
            st.success(message)

            encoding_message = save_all_encodings()
            st.success(encoding_message)

            st.rerun()

    with col2:

        if st.button("❌ Cancel"):

            st.rerun()


#PROJECT HEADER
st.title("🎓 Smart AI Attendance System")

st.caption(
    "AI-Powered Face Recognition Attendance Management"
)

st.divider()

st.markdown("## 🚀 Features")

feature_col1, feature_col2 = st.columns(2)

with feature_col1:

    st.write("✅ Student Registration")

    st.write("✅ Face Recognition")

    st.write("✅ Automatic Attendance")

with feature_col2:

    st.write("✅ Attendance Analytics")

    st.write("✅ Student Profile")

    st.write("✅ Unknown Face Detection")

#STUDENT REGISTATION

st.subheader("📝 Register Student")

student_name = st.text_input(
    "Enter Student Name"
)

if st.button("Register Student"):

    if student_name.strip():

        registration_dialog(student_name.strip())

    else:

        st.warning("Please enter student name.")

#START ATTENDANCE 
st.subheader("🎥 Start Attendance")

if st.button("Start Attendance"):

    st.success("Attendance System Started")

    subprocess.Popen(
        ["python", "main.py"]
    )
#LOAD ENCODINGS 
total_students = 0

student_list = []

try:

    with open("encodings.pkl", "rb") as file:

        data = pickle.load(file)

        student_list = list(data.keys())

        total_students = len(student_list)

except FileNotFoundError:

    student_list = []

    total_students = 0

#LOAD ATTENDANCE
current_year = datetime.now().year

selected_year = st.selectbox(
    "📅 Select Year",
    list(range(current_year - 5, current_year + 1)),
    index=5
)

months = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

selected_month = st.selectbox(
    "📅 Select Month",
    months,
    index=datetime.now().month - 1
)

selected_month_number = months.index(selected_month) + 1

# -------------------------
# NOW load attendance
# -------------------------

records = get_attandance()

filtered_month_records = [
    record
    for record in records
    if (
        datetime.strptime(record[2], "%Y-%m-%d").year == selected_year
        and
        datetime.strptime(record[2], "%Y-%m-%d").month == selected_month_number
    )
]

#DATE FILTER
st.subheader("🗓️ Filter Attendance")

selected_date = st.date_input(
    "Select Date"
)

date_filtered_records = [

    record

    for record in filtered_month_records

    if record[2] == str(selected_date)

]

#SEARCH STUDENT 
search_name = st.text_input(
    "🔍 Search Student"
)

display_records = date_filtered_records

if search_name:

    display_records = [

        record

        for record in display_records

        if search_name.lower()

        in record[1].lower()

    ]

#ATTENDANCE TABLE
st.subheader("📋 Attendance Records")

if display_records:

    df = pd.DataFrame(

        display_records,

        columns=[
            "ID",
            "NAME",
            "DATE",
            "TIME"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        "📥 Download Attendance CSV",

        csv,

        "attendance_report.csv",

        "text/csv"

    )

else:

    st.info(
        "No attendance records found."
    )

#DASHBOARD
today = datetime.now().strftime(
    "%Y-%m-%d"
)

today_count = len(

    [

        record

        for record in records

        if record[2] == today

    ]

)

st.divider()

st.subheader("📊 Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric(

    "👥 Registered Students",

    total_students

)

col2.metric(

    "📅 Monthly Attendance",

    len(filtered_month_records)

)

col3.metric(

    "✅ Today's Attendance",

    today_count

)

#STUDENT PROFILE CARD
st.divider()

st.subheader("🆔 Student Profile")

if student_list:

    selected_student = st.selectbox(
        "Select Student",
        student_list
    )

    student_folder = os.path.join(
        "photos",
        selected_student
    )

    image_files = []

    if os.path.exists(student_folder):

        image_files = os.listdir(student_folder)

    attendance_count = sum(

        1

        for record in records

        if record[1].lower() == selected_student.lower()

    )

    last_record = None

    for record in reversed(records):

        if record[1].lower() == selected_student.lower():

            last_record = record

            break

    with st.container(border=True):

        col1, col2 = st.columns([1,2])

        with col1:

            if image_files:

                st.image(

                    os.path.join(
                        student_folder,
                        image_files[0]
                    ),

                    width=180

                )

        with col2:

            st.markdown("### 🎓 Student Information")

            st.write("**👤 Name:**", selected_student)

            st.write(

                "**🆔 Student ID:**",

                f"STU-{student_list.index(selected_student)+1:03}"

            )

            st.write(

                "**📸 Registered Images:**",

                len(image_files)

            )

            st.write(

                "**📅 Attendance Count:**",

                attendance_count

            )

            if last_record:

                st.write(

                    "**🕒 Last Attendance:**",

                    f"{last_record[2]} {last_record[3]}"

                )

            else:

                st.write(

                    "**🕒 Last Attendance:** Never"

                )

else:

    st.info(

        "No registered students found."

    )

#DELETE STUDENT 
#UNKNOWN FACES
st.divider()

st.subheader("❓ Unknown Faces")

unknown_folder = "unknown_faces"

if os.path.exists(unknown_folder):

    images = os.listdir(unknown_folder)

    if images:

        cols = st.columns(3)

        for index, image in enumerate(images):

            with cols[index % 3]:

                st.image(

                    os.path.join(

                        unknown_folder,

                        image

                    ),

                    use_container_width=True

                )

                st.caption(image)

    else:

        st.info(

            "No unknown faces found."

        )

else:

    st.info(

        "Unknown faces folder not found."

    )

#ATTENDANCE ANALYTICS
st.subheader("📊 Attendance Analytics")

attendance_count = {}

for record in filtered_month_records:

    name = record[1]

    if name not in attendance_count:
        attendance_count[name] = 0

    attendance_count[name] += 1


if attendance_count:

    col1, col2 = st.columns([3,2])

    # ----------------------------
    # Bar Chart
    # ----------------------------
    with col1:

        fig, ax = plt.subplots(figsize=(5, 3))

        ax.bar(
            attendance_count.keys(),
            attendance_count.values()
        )

        ax.set_xlabel("Students")
        ax.set_ylabel("Attendance Count")
        ax.set_title("Student Attendance")

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)

    # ----------------------------
    # Pie Chart
    # ----------------------------
    with col2:
        fig2, ax2 = plt.subplots(figsize=(4, 4))
        ax2.pie(
            attendance_count.values(),
            labels=attendance_count.keys(),
            autopct="%1.1f%%",
            startangle=90,
            radius=0.75       # Makes the pie smaller
    )

        ax2.set_title("Attendance Distribution", fontsize=14)

        st.pyplot(fig2)

else:

    st.info("No attendance data available.")
#





