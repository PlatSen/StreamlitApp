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

# --- 2. Page Title ---
st.set_page_config(
    page_title="PlatSen Birthday Tracker")

# --- 3. Current State ---
if 'shared_date' not in st.session_state:
    st.session_state.shared_date = date.today()

# --- 4. Sidebar ---
st.sidebar.title("Tracker Menu")
page = st.sidebar.selectbox("Go to:", ["Birthday List", "About"])
st.sidebar.divider()
search_query = st.sidebar.text_input("Search Name", "")
show_balloons = st.sidebar.checkbox("Enable Animations", value=True)
st.sidebar.caption("This allows balloons to pop up if the selected day is a birthday.")

# --- 5. Birthday List Page ---
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

    st.write("""    The app displays a table containing **16** people (including me) and their birthdays which are all auto sorted by date. Data in the table is **hard coded** and **uneditable**. A progress bar that reflects how far along we are through 2026 and metrics showing how many birthdays there are, how many have passed, how many have yet to pass, and what date is currently selected can also be seen on the page. 

    This has been made for my own benefit to help me remember when my cousins’ and my girlfriend have their birthdays.

    The inputs the app can collect include the **date chosen**, the **preferred input method**, a **search query**, a **note** and **page choice**.

    Through the **date chosen**, the table can show us different statuses of all of the birthdays listed by color coding them accordingly. A legend in the form of an expander can be found on top of it showing how they are color coded. If the date picked is a birthday, a celebration happens showing balloons (which are toggleable through a tick box from the sidebar) and a note is sent to the top of the table showing who the celebration is for.

    The **preferred input method** is what determines whether a **slider** or a **date picker** will be used in selecting a date to check.


    The **search query** rebuilds the table by only picking entries from the hardcoded data that include the string entered from the search box. This makes the table only show those entries making a functioning search feature.

    The **note** is from a note maker prompt that, when entered, makes a note at the bottom of the page that echoes the string submitted in the prompt.

    The **page choice** is used for determining which page you are on.""")



