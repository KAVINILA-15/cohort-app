import streamlit as st
import pandas as pd
import random

# ------------------------------
# Dummy Data
# ------------------------------
students_data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eva"],
    "Points": [120, 95, 200, 75, 150],
    "Milestone": ["Bronze", "Bronze", "Silver", "None", "Bronze"],
}
df_students = pd.DataFrame(students_data)

# Session state initialization
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "role" not in st.session_state:
    st.session_state.role = None

# ------------------------------
# Navigation Functions
# ------------------------------
def go_to(page, role=None):
    st.session_state.page = page
    st.session_state.role = role

# ------------------------------
# Welcome Page
# ------------------------------
def welcome_page():
    st.markdown("<h1 style='text-align:center; color:#4CAF50;'>🎯 Cohort Gamified Website</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>Welcome to the Cohort Ecosystem Hackathon Project</h3>", unsafe_allow_html=True)
    st.image("https://cdn.pixabay.com/photo/2016/11/29/09/08/board-1869266_1280.jpg", use_column_width=True)
    if st.button("🚀 Proceed to Login"):
        go_to("login")

# ------------------------------
# Login Page
# ------------------------------
def login_page():
    st.title("🔑 Login Page")
    role = st.radio("Select your role:", ["Student", "Mentor", "Floorwing", "Administrator"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email and password:  # Dummy check
            go_to("dashboard", role)
        else:
            st.error("Please enter email & password!")

# ------------------------------
# Student Dashboard
# ------------------------------
def student_dashboard():
    st.title("📚 Student Dashboard")
    student_points = random.choice(df_students["Points"])  # Dummy user points
    st.metric("Your Points", student_points)

    # Progress & milestones
    st.progress(min(student_points / 300, 1.0))
    if student_points >= 300:
        st.success("🏆 Milestone: Gold Achieved!")
    elif student_points >= 200:
        st.info("⭐ Milestone: Silver Achieved!")
    elif student_points >= 100:
        st.warning("🎯 Milestone: Bronze Achieved!")
    else:
        st.write("Keep going to reach your first milestone!")

    # Monthly activity chart
    st.subheader("📊 Monthly Activity")
    activity = pd.DataFrame({"Month": ["Jan", "Feb", "Mar", "Apr"], "Points": [20, 35, 50, 15]})
    st.bar_chart(activity.set_index("Month"))

    # Leaderboard
    st.subheader("🏆 Leaderboard")
    st.dataframe(df_students.sort_values("Points", ascending=False))

# ------------------------------
# Mentor Dashboard
# ------------------------------
def mentor_dashboard():
    st.title("👨‍🏫 Mentor Dashboard")
    student = st.selectbox("Select Student", df_students["Name"])
    points = st.number_input("Assign Points", min_value=0, max_value=100, step=5)
    note = st.text_area("Add Note (optional)")
    if st.button("✅ Assign Points"):
        st.success(f"{points} points assigned to {student} 🎯")
    st.subheader("📊 Current Leaderboard")
    st.table(df_students.sort_values("Points", ascending=False))

# ------------------------------
# Floorwing Dashboard
# ------------------------------
def floorwing_dashboard():
    st.title("🏢 Floorwing Dashboard")
    st.subheader("All Students in Your Floor")
    st.table(df_students)
    st.subheader("📈 Floor Performance")
    st.line_chart(df_students.set_index("Name")["Points"])

# ------------------------------
# Admin Dashboard
# ------------------------------
def admin_dashboard():
    st.title("⚙️ Administrator Dashboard")
    st.subheader("Manage All Users")
    st.dataframe(df_students)

    st.subheader("🔄 Adjust Points")
    student = st.selectbox("Choose student", df_students["Name"])
    new_points = st.number_input("Set new points", min_value=0, max_value=500, step=10)
    if st.button("Update Points"):
        st.success(f"Updated {student}'s points to {new_points}")

    st.subheader("📅 Monthly Report")
    monthly = pd.DataFrame({
        "Student": df_students["Name"],
        "Monthly Points": [random.randint(50, 150) for _ in range(len(df_students))]
    })
    st.bar_chart(monthly.set_index("Student"))

# ------------------------------
# Routing Logic
# ------------------------------
if st.session_state.page == "welcome":
    welcome_page()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "dashboard":
    role = st.session_state.role
    if role == "Student":
        student_dashboard()
    elif role == "Mentor":
        mentor_dashboard()
    elif role == "Floorwing":
        floorwing_dashboard()
    elif role == "Administrator":
        admin_dashboard()
