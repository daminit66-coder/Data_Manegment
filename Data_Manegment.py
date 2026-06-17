import streamlit as st
import json
from pathlib import Path
import pandas as pd

DATABASE = "clg_data.json"

# ---------------- Load Data ----------------
data = {"students": [], "teachers": []}

if Path(DATABASE).exists():
    try:
        with open(DATABASE, "r") as f:
            content = f.read().strip()
            if content:
                data = json.loads(content)
    except:
        data = {"students": [], "teachers": []}


def save():
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------- Page Config ----------------
st.set_page_config(
    page_title="College Management System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 College Management System")
st.markdown("---")

menu = st.sidebar.selectbox(
    "Choose Option",
    [
        "Register Student",
        "Register Teacher",
        "Add Grades",
        "Show Students",
        "Show Teachers",
        "Delete Student",
        "Delete Teacher"
    ]
)

# ---------------- Register Student ----------------
if menu == "Register Student":
    st.header("➕ Register Student")

    name = st.text_input("Student Name")
    year = st.selectbox(
        "Year",
        ["1st Year", "2nd Year", "3rd Year", "4th Year"]
    )
    email = st.text_input("Email")
    rn = st.number_input("Roll Number", min_value=1)

    if st.button("Register Student"):
        if "@" not in email:
            st.error("Invalid Email")
        else:
            found = False
            for s in data["students"]:
                if s["roll number"] == rn:
                    found = True
                    break

            if found:
                st.warning("Student already exists.")
            else:
                data["students"].append({
                    "name": name,
                    "mail": email,
                    "year": year,
                    "roll number": rn,
                    "grade": {}
                })
                save()
                st.success("Student Registered Successfully!")

# ---------------- Register Teacher ----------------
elif menu == "Register Teacher":
    st.header("👨‍🏫 Register Teacher")

    name = st.text_input("Teacher Name")
    subject = st.text_input("Subject")
    email = st.text_input("Email")
    tid = st.number_input("Teacher ID", min_value=1)

    if st.button("Register Teacher"):
        if "@" not in email:
            st.error("Invalid Email")
        else:
            found = False
            for t in data["teachers"]:
                if t["id"] == tid:
                    found = True
                    break

            if found:
                st.warning("Teacher already exists.")
            else:
                data["teachers"].append({
                    "name": name,
                    "mail": email,
                    "subject": subject,
                    "id": tid
                })
                save()
                st.success("Teacher Registered Successfully!")

# ---------------- Add Grades ----------------
elif menu == "Add Grades":
    st.header("📝 Add Grades")

    rn = st.number_input("Roll Number", min_value=1)
    subject = st.text_input("Subject")
    marks = st.number_input("Marks", min_value=0.0, max_value=100.0)

    if st.button("Add Grade"):
        found = False
        for s in data["students"]:
            if s["roll number"] == rn:
                s["grade"][subject] = marks
                save()
                found = True
                st.success("Grade Added Successfully!")

        if not found:
            st.error("Student Not Found")

# ---------------- Show Students ----------------
elif menu == "Show Students":
    st.header("📚 Students List")

    if data["students"]:
        df = pd.DataFrame(data["students"])
        st.dataframe(df)
    else:
        st.info("No students found.")

# ---------------- Show Teachers ----------------
elif menu == "Show Teachers":
    st.header("👨‍🏫 Teachers List")

    if data["teachers"]:
        df = pd.DataFrame(data["teachers"])
        st.dataframe(df)
    else:
        st.info("No teachers found.")

# ---------------- Delete Student ----------------
elif menu == "Delete Student":
    st.header("❌ Delete Student")

    rn = st.number_input("Enter Roll Number", min_value=1)

    if st.button("Delete Student"):
        for s in data["students"]:
            if s["roll number"] == rn:
                data["students"].remove(s)
                save()
                st.success("Student Deleted Successfully!")
                break
        else:
            st.error("Student Not Found")

# ---------------- Delete Teacher ----------------
elif menu == "Delete Teacher":
    st.header("❌ Delete Teacher")

    tid = st.number_input("Enter Teacher ID", min_value=1)

    if st.button("Delete Teacher"):
        for t in data["teachers"]:
            if t["id"] == tid:
                data["teachers"].remove(t)
                save()
                st.success("Teacher Deleted Successfully!")
                break
        else:
            st.error("Teacher Not Found")

st.sidebar.markdown("---")
st.sidebar.info(
    "🎓 College Management System\n\nDeveloped using Python & Streamlit"
)