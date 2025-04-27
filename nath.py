
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from datetime import datetime
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# # ---- Settings ----
# ADMIN_PASSWORD = "Akwasiwusu"

# # ---- Email Sending Setup ----
# SENDER_EMAIL = "vicentiaemuah21@gmail.com"  
# SENDER_PASSWORD = "VICENTIA2002"     

# def send_confirmation_email(receiver_email, member_name):
#     subject = "Adventist Church Registration Successful 🎉"
#     body = f"""
#     Dear {member_name},

#     Thank you for registering with the Adventist Church Membership System!

#     We are happy to have you as part of our community. 
#     God richly bless you! 🙏

#     Date & Time of Registration: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

#     Kind Regards, 
#     Adventist Church Membership Team
#     """

#     message = MIMEMultipart()
#     message['From'] = SENDER_EMAIL
#     message['To'] = receiver_email
#     message['Subject'] = subject

#     message.attach(MIMEText(body, 'plain'))

#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#         server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
#         server.quit()
#         print("Email sent successfully!")
#     except Exception as e:
#         print(f"Failed to send email: {e}")

# # ---- Session Setup ----
# if 'members' not in st.session_state:
#     st.session_state.members = []

# if 'is_admin' not in st.session_state:
#     st.session_state.is_admin = False

# # ---- Page Setup ----
# st.set_page_config(page_title="Adventist Church Membership Registration System", layout="centered")

# # Logo and Title in a single full-width column
# st.image("LOGO.jpg", width=800)
# st.title("⛪ Adventist Church Membership Registration System")

# # ---- Sidebar for Admin Login ----
# with st.sidebar:
#     st.markdown("### 🔒 Admin Login")
#     password = st.text_input("Enter Admin Password", type="password")
#     if st.button("Login as Admin"):
#         if password == ADMIN_PASSWORD:
#             st.session_state.is_admin = True
#             st.success("✅ Admin access granted!")
#         else:
#             st.error("❌ Incorrect password.")

# # ---- Main Content Area ----
# col1, col2 = st.columns([2, 130])  #

# # ---- Member Registration Form in the second column ----
# with col2:
#     st.markdown("### 📝 Register Here")
#     with st.form("member_form"):
#         name = st.text_input("Full Name")
#         student_id = st.text_input("Student ID")
#         index_number = st.text_input("Index Number")
#         phone = st.text_input("Phone Number")
#         residence = st.text_input("Place of Residence")
#         gmail = st.text_input("Gmail Address")
#         course = st.text_input("Course")
#         level = st.selectbox("Level", ["", "100", "200", "300", "400", "Graduate"])

#         submitted = st.form_submit_button("Submit")

#         registered_gmails = [m['Gmail'] for m in st.session_state.members]

#         if submitted:
#             if not all([name, student_id, index_number, phone, residence, gmail, course, level]):
#                 st.warning("⚠️ Please complete all fields.")
#             elif gmail in registered_gmails:
#                 st.error("🔁 You have already registered with this Gmail.")
#             else:
#                 timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                 st.session_state.members.append({
#                     "Name": name,
#                     "Student ID": student_id,
#                     "Index Number": index_number,
#                     "Phone Number": phone,
#                     "Residence": residence,
#                     "Gmail": gmail,
#                     "Course": course,
#                     "Level": level,
#                     "Timestamp": timestamp
#                 })
#                 st.success("✅ Submitted successfully. God bless you!")
#                 st.balloons()

#                 # Send Confirmation Email
#                 send_confirmation_email(gmail, name)

# # ---- Admin Dashboard (Only visible when logged in) ----
# if st.session_state.is_admin:
#     st.markdown("---")
#     st.header("📋 Admin Dashboard")

#     df = pd.DataFrame(st.session_state.members)

#     search_query = st.text_input("🔍 Search Members", "")
#     if search_query:
#         df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

#     if not df.empty:
#         st.subheader("👥 All Registered Members")
#         st.dataframe(df)

#         st.subheader("📚 Grouped Members by Course and Level")
#         grouped = df.groupby(['Course', 'Level'])
#         for (course, level), group in grouped:
#             st.markdown(f"### 📘 {course} - Level {level}")
#             st.dataframe(group.reset_index(drop=True))

#         st.subheader("📊 Summary Statistics")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.markdown("**📌 Members per Course**")
#             st.dataframe(df['Course'].value_counts())
#         with col2:
#             st.markdown("**🎓 Members per Level**")
#             st.dataframe(df['Level'].value_counts())

#         st.subheader("🥧 Pie Chart: Students by Level")
#         level_counts = df['Level'].value_counts().reset_index()
#         level_counts.columns = ['Level', 'Count']
#         fig = px.pie(level_counts, names='Level', values='Count', title='Student Level Distribution')
#         st.plotly_chart(fig)

#         st.subheader("⬇️ Export Data")
#         csv = df.to_csv(index=False).encode('utf-8')
#         st.download_button("Download CSV", csv, "church_members.csv", "text/csv")

#         # --- Remove Member Section ---
#         st.markdown("---")
#         st.subheader("🗑️ Remove a Member")

#         if st.session_state.members:
#             remove_by = st.selectbox("Select how to remove", ["Name", "Gmail"])

#             if remove_by == "Name":
#                 member_names = [member["Name"] for member in st.session_state.members]
#                 selected_member = st.selectbox("Select Member by Name", member_names)
#             elif remove_by == "Gmail":
#                 member_gmails = [member["Gmail"] for member in st.session_state.members]
#                 selected_member = st.selectbox("Select Member by Gmail", member_gmails)

#             if st.button("Remove Selected Member"):
#                 new_members = []
#                 for member in st.session_state.members:
#                     if (remove_by == "Name" and member["Name"] != selected_member) or \
#                        (remove_by == "Gmail" and member["Gmail"] != selected_member):
#                         new_members.append(member)
#                 st.session_state.members = new_members
#                 st.success(f"✅ Member '{selected_member}' has been removed successfully.")
#         else:
#             st.info("ℹ️ No members to remove.")

#     else:
#         st.info("ℹ️ No members have registered yet.")





import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# ---- Settings ----
ADMIN_PASSWORD = "Akwasiwusu"
DATABASE_FILE = "members.csv"  # CSV file to store registrations

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
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# ---- Load Existing Members from CSV ----
if os.path.exists(DATABASE_FILE):
    df_members = pd.read_csv(DATABASE_FILE)
else:
    df_members = pd.DataFrame(columns=["Name", "Student ID", "Index Number", "Phone Number", "Residence", "Gmail", "Course", "Level", "Timestamp"])

# ---- Session Setup ----
if 'members' not in st.session_state:
    st.session_state.members = df_members.to_dict('records')

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# ---- Page Setup ----
st.set_page_config(page_title="Adventist Church Membership Registration System", layout="centered")

# Logo and Title
st.image("LOGO.jpg", width=800)
st.title("⛪ Adventist Church Membership Registration System")

# ---- Sidebar for Admin Login ----
with st.sidebar:
    if not st.session_state.is_admin:
        st.markdown("### 🔒 Admin Login")
        password = st.text_input("Enter Admin Password", type="password")
        if st.button("Login as Admin"):
            if password == ADMIN_PASSWORD:
                st.session_state.is_admin = True
                st.success("✅ Admin access granted!")
            else:
                st.error("❌ Incorrect password.")
    else:
        if st.button("🚪 Logout"):
            st.session_state.is_admin = False
            st.success("✅ Logged out successfully!")
            st.experimental_rerun()

# ---- Main Content Area ----
col1, col2 = st.columns([2, 130])

# ---- Member Registration Form in the second column ----
with col2:
    st.markdown("### 📝 Register Here")
    with st.form("member_form"):
        name = st.text_input("Full Name")
        student_id = st.text_input("Student ID")
        index_number = st.text_input("Index Number")
        phone = st.text_input("Phone Number")
        residence = st.text_input("Place of Residence")
        gmail = st.text_input("Gmail Address")
        course = st.text_input("Course")
        level = st.selectbox("Level", ["", "100", "200", "300", "400", "Graduate"])

        submitted = st.form_submit_button("Submit")

        registered_gmails = [m['Gmail'] for m in st.session_state.members]

        if submitted:
            if not all([name, student_id, index_number, phone, residence, gmail, course, level]):
                st.warning("⚠️ Please complete all fields.")
            elif gmail in registered_gmails:
                st.error("🔁 You have already registered with this Gmail.")
            else:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_member = {
                    "Name": name,
                    "Student ID": student_id,
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
                updated_df = pd.DataFrame(st.session_state.members)
                updated_df.to_csv(DATABASE_FILE, index=False)

                # Send Confirmation Email
                send_confirmation_email(gmail, name)

# ---- Admin Dashboard (Only visible when logged in) ----
if st.session_state.is_admin:
    st.markdown("---")
    st.header("📋 Admin Dashboard")

    df = pd.DataFrame(st.session_state.members)

    search_query = st.text_input("🔍 Search Members", "")
    if search_query:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

    if not df.empty:
        st.subheader("👥 All Registered Members")

        for i, member in df.iterrows():
            member_info = f"{member['Name']} ({member['Gmail']}) - {member['Course']} Level {member['Level']}"
            col1, col2, col3 = st.columns([5, 1, 1])
            with col1:
                st.write(member_info)
            with col2:
                if st.button(f"Remove {i}", key=f"remove_{i}"):
                    st.session_state.members.pop(i)
                    updated_df = pd.DataFrame(st.session_state.members)
                    updated_df.to_csv(DATABASE_FILE, index=False)
                    st.success(f"✅ Member '{member['Name']}' removed successfully!")
                    st.experimental_rerun()
            with col3:
                if st.button(f"Edit {i}", key=f"edit_{i}"):
                    st.session_state.edit_index = i
                    st.experimental_rerun()

        if st.session_state.edit_index is not None:
            st.subheader("✏️ Edit Member Details")
            member = st.session_state.members[st.session_state.edit_index]
            with st.form("edit_form"):
                name = st.text_input("Full Name", member['Name'])
                student_id = st.text_input("Student ID", member['Student ID'])
                index_number = st.text_input("Index Number", member['Index Number'])
                phone = st.text_input("Phone Number", member['Phone Number'])
                residence = st.text_input("Place of Residence", member['Residence'])
                gmail = st.text_input("Gmail Address", member['Gmail'])
                course = st.text_input("Course", member['Course'])
                level = st.selectbox("Level", ["100", "200", "300", "400", "Graduate"], index=["100", "200", "300", "400", "Graduate"].index(member['Level']))
                submitted_edit = st.form_submit_button("Save Changes")

                if submitted_edit:
                    st.session_state.members[st.session_state.edit_index] = {
                        "Name": name,
                        "Student ID": student_id,
                        "Index Number": index_number,
                        "Phone Number": phone,
                        "Residence": residence,
                        "Gmail": gmail,
                        "Course": course,
                        "Level": level,
                        "Timestamp": member['Timestamp']  # Keep original timestamp
                    }
                    updated_df = pd.DataFrame(st.session_state.members)
                    updated_df.to_csv(DATABASE_FILE, index=False)
                    st.success(f"✅ Member '{name}' updated successfully!")
                    st.session_state.edit_index = None
                    st.experimental_rerun()

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
        st.info("ℹ️ No members have registered yet.")
