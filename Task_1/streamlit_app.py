
import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:5000/students"

st.set_page_config(page_title="Student Management", page_icon="🎓")
st.title("🎓 Student Management System")

menu = st.sidebar.selectbox(
    "Choose Operation",
    ["View Students", "Add Student", "Update Student", "Delete Student"]
)

if menu == "View Students":
    st.header("View Students")
    if st.button("Load Students"):
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                students = response.json()
                if students:
                    st.dataframe(pd.DataFrame(students), use_container_width=True)
                else:
                    st.info("No students found.")
            else:
                st.error("Unable to load students.")
        except requests.exceptions.RequestException:
            st.error("Start the Flask API first.")

elif menu == "Add Student":
    st.header("Add Student")
    with st.form("add_form"):
        name = st.text_input("Student Name")
        department = st.text_input("Department")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Add Student")

        if submitted:
            if name and department and email:
                try:
                    response = requests.post(
                        API_URL,
                        json={
                            "name": name,
                            "department": department,
                            "email": email
                        }
                    )
                    if response.status_code == 201:
                        st.success("Student added successfully!")
                    else:
                        st.error(response.json().get("error", "Could not add student."))
                except requests.exceptions.RequestException:
                    st.error("Start the Flask API first.")
            else:
                st.warning("Please fill all fields.")

elif menu == "Update Student":
    st.header("Update Student")
    with st.form("update_form"):
        student_id = st.number_input("Student ID", min_value=1, step=1)
        name = st.text_input("New Name")
        department = st.text_input("New Department")
        email = st.text_input("New Email")
        submitted = st.form_submit_button("Update Student")

        if submitted:
            if name and department and email:
                try:
                    response = requests.put(
                        f"{API_URL}/{student_id}",
                        json={
                            "name": name,
                            "department": department,
                            "email": email
                        }
                    )
                    if response.status_code == 200:
                        st.success("Student updated successfully!")
                    else:
                        st.error(response.json().get("error", "Could not update student."))
                except requests.exceptions.RequestException:
                    st.error("Start the Flask API first.")
            else:
                st.warning("Please fill all fields.")

elif menu == "Delete Student":
    st.header("Delete Student")
    student_id = st.number_input("Student ID to Delete", min_value=1, step=1)

    if st.button("Delete Student"):
        try:
            response = requests.delete(f"{API_URL}/{student_id}")
            if response.status_code == 200:
                st.success("Student deleted successfully!")
            else:
                st.error(response.json().get("error", "Could not delete student."))
        except requests.exceptions.RequestException:
            st.error("Start the Flask API first.")
