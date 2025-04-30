import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sqlite3

# ---- Settings ----
ADMIN_PASSWORD = "Akwasiwusu"
DATABASE_FILE = "members.csv"  # This is the CSV file to store registrations
DATABASE_SQLITE = "members.db"  # SQLite Database

# ---- Email Sending Setup ----
SENDER_EMAIL = "vicentiaemuah21@gmail.com"  
SENDER_PASSWORD = "VICENTIA2002"  # ⚠️ Consider using environment variables instead of hardcoding

def send_confirmation_email(receiver_email, member_name):
    subject = "Adventist Church Registration Successful 🎉"
    body = f"""
    Dear {member_name},

    Thank you for registering with the Adventist Church Membership System!

    We are happy to have you as part of our community. 
    God richly bless you! 🙏

    Date & Time of Registration: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    Kind Regards, 
    Adventist Church Membership Team
    """

    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

# ---- SQLite Database Setup ----
def create_table():
    conn = sqlite3.connect(DATABASE_SQLITE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        index_number TEXT,
                        phone TEXT,
                        residence TEXT,
                        gmail TEXT UNIQUE,
                        course TEXT,
                        level TEXT,
                        timestamp TEXT)''')
    conn.commit()
    conn.close()

create_table()

def add_member_to_sqlite(member):
    conn = sqlite3.connect(DATABASE_SQLITE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO members (name, index_number, phone, residence, gmail, course, level, timestamp) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (member["Name"], member["Index Number"], member["Phone Number"], 
                    member["Residence"], member["Gmail"], member["Course"], member["Level"], member["Timestamp"]))
    conn.commit()
    conn.close()

def load_members_from_sqlite():
    conn = sqlite3.connect(DATABASE_SQLITE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, index_number, phone, residence, gmail, course, level, timestamp FROM members")
    members = cursor.fetchall()
    conn.close()
    return members

# ---- Set Page Config ----
st.set_page_config(page_title="Adventist Church Membership Registration System", layout="centered")

# ---- Load CSV File (if exists) ----
df_members = pd.DataFrame(columns=["Name", "Index Number", "Phone Number", "Residence", "Gmail", "Course", "Level", "Timestamp"])

# Only try to load CSV if it exists
if os.path.exists(DATABASE_FILE):
    try:
        df_members = pd.read_csv(DATABASE_FILE)
        if df_members.empty:
            st.warning("⚠️ The CSV file is empty. No data to display.")
    except pd.errors.EmptyDataError:
        st.warning("⚠️ The CSV file is empty or improperly formatted.")
    except Exception as e:
        st.error(f"An error occurred while reading the CSV file: {str(e)}")

# ---- Session State ----
if 'members' not in st.session_state:
    st.session_state.members = df_members.to_dict('records')

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# ---- App UI ----
st.image("LOGO.jpg", width=800)
st.title("⛪ Adventist Church Membership Registration System")

# ---- Admin Login ----
with st.sidebar:
    st.markdown("### 🔒 Admin Login")
    password = st.text_input("Enter Admin Password", type="password")
    if st.button("Login as Admin"):
        if password == ADMIN_PASSWORD:
            st.session_state.is_admin = True
            st.success("✅ Admin access granted!")
        else:
            st.error("❌ Incorrect password.")

# ---- Registration Form ----
col1, col2 = st.columns([2, 130])
with col2:
    st.markdown("### 📝 Register Here")
    with st.form("member_form"):
        name = st.text_input("Full Name")
        index_number = st.text_input("Index Number")
        phone = st.text_input("Phone Number")
        residence = st.text_input("Place of Residence")
        gmail = st.text_input("Gmail Address")
        course = st.text_input("Course")
        level = st.selectbox("Level", ["", "100", "200", "300", "400", "Graduate"])

        submitted = st.form_submit_button("Submit")
        registered_gmails = [m['Gmail'] for m in st.session_state.members]

        if submitted:
            if not all([name, index_number, phone, residence, gmail, course, level]):
                st.warning("⚠️ Please complete all fields.")
            elif gmail in registered_gmails:
                st.error("🔁 You have already registered with this Gmail.")
            else:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_member = {
                    "Name": name,
                    "Index Number": index_number,
                    "Phone Number": phone,
                    "Residence": residence,
                    "Gmail": gmail,
                    "Course": course,
                    "Level": level,
                    "Timestamp": timestamp
                }
                st.session_state.members.append(new_member)
                st.success("✅ Submitted successfully. God bless you!")
                st.balloons()

                pd.DataFrame(st.session_state.members).to_csv(DATABASE_FILE, index=False)
                add_member_to_sqlite(new_member)
                send_confirmation_email(gmail, name)

# ---- Admin Dashboard ----
if st.session_state.is_admin:
    st.markdown("---")
    st.header("📋 Admin Dashboard")

    members_from_sqlite = load_members_from_sqlite()

    if members_from_sqlite:
        df = pd.DataFrame(members_from_sqlite, columns=["ID", "Name", "Index Number", "Phone Number", "Residence", "Gmail", "Course", "Level", "Timestamp"])

        search_query = st.text_input("🔍 Search Members", "")
        if search_query:
            df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

        if not df.empty:
            st.subheader("👥 All Registered Members")
            st.dataframe(df)

            st.subheader("📚 Grouped Members by Course and Level")
            grouped = df.groupby(['Course', 'Level'])
            for (course, level), group in grouped:
                st.markdown(f"### 📘 {course} - Level {level}")
                st.dataframe(group.reset_index(drop=True))

            st.subheader("📊 Summary Statistics")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📌 Members per Course**")
                st.dataframe(df['Course'].value_counts())
            with col2:
                st.markdown("**🎓 Members per Level**")
                st.dataframe(df['Level'].value_counts())

            st.subheader("🥧 Pie Chart: Students by Level")
            level_counts = df['Level'].value_counts().reset_index()
            level_counts.columns = ['Level', 'Count']
            fig = px.pie(level_counts, names='Level', values='Count', title='Student Level Distribution')
            st.plotly_chart(fig)

            st.subheader("⬇️ Export Data")
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "church_members.csv", "text/csv")

        else:
            st.info("ℹ️ No members found with the search query.")
    else:
        st.info("ℹ️ No members have registered yet.")

    # ---- Remove Member Section ----
    st.markdown("---")
    st.subheader("🗑️ Remove a Member")
    if st.session_state.members:
        remove_by = st.selectbox("Select how to remove", ["Name", "Gmail"])
        selected_member = None

        if remove_by == "Name":
            member_names = [member["Name"] for member in st.session_state.members]
            selected_member = st.selectbox("Select Member by Name", member_names)
        elif remove_by == "Gmail":
            member_gmails = [member["Gmail"] for member in st.session_state.members]
            selected_member = st.selectbox("Select Member by Gmail", member_gmails)

        if st.button("Remove Selected Member"):
            new_members = [member for member in st.session_state.members if member[remove_by] != selected_member]
            st.session_state.members = new_members
            pd.DataFrame(new_members).to_csv(DATABASE_FILE, index=False)
            st.success(f"✅ Member '{selected_member}' has been removed successfully.")
    else:
        st.info("ℹ️ No members to remove.")
