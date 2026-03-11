import streamlit as st
import pandas as pd
from datetime import date

# --- 1. Birthdays ---
data = {
    "Name": [
        "Ate Angel", "Purpy", "Velvet", "Kuya Adii", "Ate Ysha", "Ate Via", 
        "Peachy", "Kuya Yvo", "Amber", "Lilac", "Kuya Red", "Kuya Pao", 
        "Danda", "King", "Kuya Aaron", "CJ"
    ],
    "Birthday": [
        date(2026, 1, 5),   date(2026, 1, 9),   date(2026, 2, 8),   
        date(2026, 2, 10),  date(2026, 2, 28),  date(2026, 4, 8),   
        date(2026, 4, 14),  date(2026, 5, 3),   date(2026, 6, 19),  
        date(2026, 7, 29),  date(2026, 9, 5),   date(2026, 10, 22), 
        date(2026, 10, 30), date(2026, 11, 1),  date(2026, 12, 5),  
        date(2026, 12, 25)
    ]
}
df = pd.DataFrame(data).sort_values(by="Birthday")

# --- 2. Current State ---
if 'shared_date' not in st.session_state:
    st.session_state.shared_date = date.today()

# --- 3. Sidebar ---
st.sidebar.title("Tracker Menu")
page = st.sidebar.selectbox("Go to:", ["Birthday List", "About"])
st.sidebar.divider()
search_query = st.sidebar.text_input("Search Name", "")
show_balloons = st.sidebar.checkbox("Enable Animations", value=True)
st.sidebar.caption("This allows balloons to pop up if the selected day is a birthday.")

# --- 4. Birthday List Page ---
if page == "Birthday List":
    st.title("2026 Family Birthday Tracker")

    # Progress Bar 
    today = date.today()
    day_of_year = today.timetuple().tm_yday
    st.progress(day_of_year / 365, text=f"Year progress: {int((day_of_year/365)*100)}%")

    # Main Page Switcher
    input_method = st.radio("Date Input Method:", ("Slider", "Date Picker"), horizontal=True)

    # Date Selection (Using 'key' to sync the slider and picker without double-clicks)
    if input_method == "Slider":
        st.slider(
            "Select reference date:", date(2026, 1, 1), date(2026, 12, 31), 
            key="shared_date", format="MMM DD"
        )
    else:
        # Note: st.date_input also uses the 'shared_date' key to stay in sync
        st.date_input("Pick a reference date:", key="shared_date")

    selected_date = st.session_state.shared_date

    # Metrics
    passed_bdays = df[df['Birthday'] < selected_date].shape[0]
    upcoming_count = len(df) - passed_bdays

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total", len(df))
    m2.metric("Passed", passed_bdays)
    m3.metric("Upcoming", upcoming_count)
    m4.metric("Selected", selected_date.strftime("%b %d"))

    # Table & Search
    display_df = df.copy()
    if search_query:
        display_df = display_df[display_df['Name'].str.contains(search_query, case=False)]

    with st.expander("Table Legend"):
        st.write("Green: Passed | Blue: Birthday Today | Yellow: Upcoming")

    def apply_colors(row):
        if row['Birthday'] < selected_date:
            return ['background-color: #d4edda; color: #155724'] * len(row)
        elif row['Birthday'] == selected_date:
            return ['background-color: #d6d4ed; color: #181557'] * len(row)
        return ['background-color: #fff3cd; color: #856404'] * len(row)
        
    # Celebration logic
    if selected_date in df['Birthday'].values:
        celebrant = df[df['Birthday'] == selected_date]['Name'].values[0]
        if show_balloons:
            st.balloons()
        st.success(f"Today is {celebrant}'s Birthday")

    st.table(display_df.style.apply(apply_colors, axis=1))

    # Note Maker
    prompt = st.chat_input("Write a note...")
    if prompt:
        st.info(f"Note: {prompt}")

elif page == "About":
    st.title("About")
    st.divider()
    st.write("This application monitors family milestones for the year **2026**.")