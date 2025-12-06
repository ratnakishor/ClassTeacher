import streamlit as st
import pandas as pd
import pywhatkit
import time
import tempfile

st.set_page_config(page_title="WhatsApp Attendance Sender", layout="wide")


st.sidebar.title("Template & Options")

try:
    with open(r"data.xlsx", "rb") as f:
        file_bytes = f.read()

    st.sidebar.download_button(
    label="📥 Download Excel Template",
    data=file_bytes,
    file_name="data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
except FileNotFoundError:
    st.sidebar.error("❌ data.xlsx not found in app directory.")

st.title("📚 WhatsApp Attendance Message Sender")

st.write("Upload an Excel file and send automated WhatsApp messages to absent students.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

df = pd.DataFrame()


if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("### Preview of Uploaded Data:")
    st.dataframe(df)

    # Check required columns
    required_cols = {"Name", "Parent Number", "Date", "Attendance"}
    if not required_cols.issubset(df.columns):
        st.error(f"Excel must contain columns: {required_cols}")
    else:
        st.success("Excel format is valid.")

        default_message = (
            "Dear Parent,\n\n"
            "Your child *{name}* is absent today ({date}).\n\n"
            "-- Sasi Institute of Technology & Engineering"
        )

        st.write("### Message Template (Variables: {name}, {date})")
        message_template = st.text_area("Edit Message Template", default_message, height=150)

# Initialize session state for button
if "run_clicked" not in st.session_state:
    st.session_state.msgs_sent = False


st.warning("WhatsApp Web will open. Keep your phone connected to the Internet.")


if st.button("Send WhatsApp Messages") and not st.session_state.msgs_sent:
    
    for i, row in df.iterrows():
        if str(row['Attendance']).strip().lower() == "a":
            name = row['Name']
            mobile = "+91" + str(row['Parent Number'])
            date = str(row['Date'])
            message = message_template.format(name=name, date=date)
            try:
                #pywhatkit.sendwhatmsg_instantly(mobile, message)
                time.sleep(5)
            except Exception as e:
                st.error(f"Error sending to {mobile}: {e}")

    st.success("All messages have been processed!")
    st.session_state.msgs_sent = True

    

    



