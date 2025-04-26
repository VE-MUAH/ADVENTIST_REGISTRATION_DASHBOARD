import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---- Settings ----
ADMIN_PASSWORD = "Akwasiwusu"

# ---- Session Setup ----
if 'members' not in st.session_state:
    st.session_state.members = []

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# ---- Page Setup ----
st.set_page_config(page_title="Adventist Membership System", layout="centered")
st.title("⛪ Adventist Church Membership System")

# ---- Sidebar for Admin Login ----
with st.sidebar:
    st.markdown("### 🔒 Admin Login")
    password = st.text_input("Enter Admin Password", type="password")
    if st.button("Login as Admin"):
        if password == ADMIN_PASSWORD:
            st.session_state.is_admin = True
            st.success("✅ Admin access granted!")
        else:
            st.error("❌ Incorrect password.")

# ---- Main Content Area ----
col1, col2 = st.columns(2)

# ---- Member Registration ----
with col2:
    st.markdown("### 📝 Member Registration")
    with st.form("member_form"):
        name = st.text_input("Full Name")
        student_id = st.text_input("Student ID")
        index_number = st.text_input("Index Number")
        phone = st.text_input("Phone Number")
        residence = st.text_input("Place of Residence")
        gmail = st.text_input("Gmail Address")
        course = st.text_input("Course")
        level = st.selectbox("Level", ["","100", "200", "300", "400", "Graduate"])

        submitted = st.form_submit_button("Submit")
        # clear_clicked = st.form_submit_button("Clear Form")

        # Duplicate Check
        registered_gmails = [m['Gmail'] for m in st.session_state.members]

        if submitted:
            if not all([name, student_id, index_number, phone, residence, gmail, course, level]):
                st.warning("⚠️ Please complete all fields.")
            elif gmail in registered_gmails:
                st.error("🔁 You have already registered with this Gmail.")
            else:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                st.session_state.members.append({
                    "Name": name,
                    "Student ID": student_id,
                    "Index Number": index_number,
                    "Phone Number": phone,
                    "Residence": residence,
                    "Gmail": gmail,
                    "Course": course,
                    "Level": level,
                    "Timestamp": timestamp
                })
                st.success("✅ Submitted successfully. God bless you!")

        # Clear form feedback (just resets visuals, can't reset input fields in Streamlit natively)
        # if clear_clicked:
        #     st.session_state.members = []  
        #     st.success("Form has been cleared!") 

# ---- Admin Dashboard (Only visible when logged in) ----
if st.session_state.is_admin:
    st.markdown("---")
    st.header("📋 Admin Dashboard")

    df = pd.DataFrame(st.session_state.members)

    # Search Box for Admin Dashboard
    search_query = st.text_input("🔍 Search Members", "")
    if search_query:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

    if not df.empty:
        st.subheader("👥 All Registered Members")
        st.dataframe(df)

        # Grouped Members
        st.subheader("📚 Grouped Members by Course and Level")
        grouped = df.groupby(['Course', 'Level'])
        for (course, level), group in grouped:
            st.markdown(f"### 📘 {course} - Level {level}")
            st.dataframe(group.reset_index(drop=True))

        # Summary Stats
        st.subheader("📊 Summary Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📌 Members per Course**")
            st.dataframe(df['Course'].value_counts())
        with col2:
            st.markdown("**🎓 Members per Level**")
            st.dataframe(df['Level'].value_counts())

        # Pie Chart for Level Distribution
        st.subheader("🥧 Pie Chart: Students by Level")
        level_counts = df['Level'].value_counts().reset_index()
        level_counts.columns = ['Level', 'Count']
        fig = px.pie(level_counts, names='Level', values='Count', title='Student Level Distribution')
        st.plotly_chart(fig)

        # Export
        st.subheader("⬇️ Export Data")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "church_members.csv", "text/csv")

    else:
        st.info("ℹ️ No members have registered yet.")



