
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
DATABASE_FILE = "members.csv"  # CSV storage
DATABASE_SQLITE = "members.db"  # SQLite Database

# ---- Email Sending Setup ----
SENDER_EMAIL = "vicentiaemuah21@gmail.com"  
SENDER_PASSWORD = "VICENTIA2002"     

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

# ---- SQLite Setup ----
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
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    conn.close()
    return members

# ---- Load Existing CSV ----
if os.path.exists(DATABASE_FILE) and os.path.getsize(DATABASE_FILE) > 0:
    try:
        df_members = pd.read_csv(DATABASE_FILE)
    except pd.errors.EmptyDataError:
        df_members = pd.DataFrame(columns=["Name", "Index Number", "Phone Number", "Residence", "Gmail", "Course", "Level", "Timestamp"])
else:
    df_members = pd.DataFrame(columns=["Name", "Index Number", "Phone Number", "Residence", "Gmail", "Course", "Level", "Timestamp"])

# ---- Session State ----
if 'members' not in st.session_state:
    st.session_state.members = df_members.to_dict('records')

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

st.set_page_config(page_title="Adventist Church Membership Registration System", layout="centered")

# ---- Page ----
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

col1, col2 = st.columns([2, 130])

# ---- Member Registration ----
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

                # Save to CSV
                pd.DataFrame(st.session_state.members).to_csv(DATABASE_FILE, index=False)

                # Save to SQLite
                add_member_to_sqlite(new_member)

                # Send email
                send_confirmation_email(gmail, name)

# ---- Admin Dashboard ----
if st.session_state.is_admin:
    st.markdown("---")
    st.header("📋 Admin Dashboard")
    members_from_sqlite = load_members_from_sqlite()
    print(members_from_sqlite) 

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
                st.dataframe(df['Course'].value_counts().reset_index().rename(columns={"index": "Course", "Course": "Count"}))
            with col2:
                st.markdown("**🎓 Members per Level**")
                st.dataframe(df['Level'].value_counts().reset_index().rename(columns={"index": "Level", "Level": "Count"}))

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

    # ---- Remove Member ----
    st.markdown("---")
    st.subheader("🗑️ Remove a Member")

    if st.session_state.members:
        remove_by = st.selectbox("Select how to remove", ["Name", "Gmail"])
        selected_member = None

        if remove_by == "Name":
            names = [member["Name"] for member in st.session_state.members]
            selected_member = st.selectbox("Select Member by Name", names)
        elif remove_by == "Gmail":
            gmails = [member["Gmail"] for member in st.session_state.members]
            selected_member = st.selectbox("Select Member by Gmail", gmails)

        if st.button("Remove Selected Member"):
            # Remove from session state
            new_members = [
                m for m in st.session_state.members 
                if not ((remove_by == "Name" and m["Name"] == selected_member) or
                        (remove_by == "Gmail" and m["Gmail"] == selected_member))
            ]
            st.session_state.members = new_members

            # Remove from SQLite database
            conn = sqlite3.connect(DATABASE_SQLITE)
            cursor = conn.cursor()
            if remove_by == "Name":
                cursor.execute("DELETE FROM members WHERE name = ?", (selected_member,))
            elif remove_by == "Gmail":
                cursor.execute("DELETE FROM members WHERE gmail = ?", (selected_member,))
            conn.commit()
            conn.close()

            # Update the CSV file
            pd.DataFrame(new_members).to_csv(DATABASE_FILE, index=False)

            st.success(f"✅ Member '{selected_member}' has been removed successfully!")
        else:
            st.info("ℹ️ No members to remove.")

