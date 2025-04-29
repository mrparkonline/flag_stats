import streamlit as st
import gspread
import pandas as pd

# Initialization
google_service_account_info = st.secrets["google_service_account"]
gc = gspread.service_account_from_dict(google_service_account_info)
stat_sheet = gc.open_by_key(st.secrets['sheet_link']['key'])
responses = stat_sheet.get_worksheet(0)
all_stats = responses.get_all_records()
stat_df = pd.DataFrame(all_stats).replace('', 0)

st.set_page_config(
    page_title="JR Flag Stats",
    page_icon=":football:",
    layout="wide"
)
# End of Initialzations

# PASSING DATA
passing_cols = ['Player', 'Passing_TD', 'Passing_OnePointConversion', 'Passing_TwoPointConversion']
pass_df = stat_df.filter(items=passing_cols).groupby('Player').sum(numeric_only=True)
pass_df = pass_df.sort_values(by='Passing_TD', ascending=False)
pass_df.columns = ['TD', '1 Point Conversions', '2 Point Conversions']

# END OF PASSING DATA

# RECEIVING DATA
rec_cols = ['Player', 'Receiving_Catches', 'Receiving_TD', 'Receiving_OnePointConversion', 'Receiving_TwoPointConversion']
rec_df = stat_df.filter(items=rec_cols).groupby('Player').sum(numeric_only=True)
rec_df = rec_df.sort_values(by='Receiving_Catches', ascending=False)
rec_df.columns = ['Receptions', 'TD', '1 Point Conversions', '2 Point Conversions']

# END OF RECEIVING DATA

# RUSHING DATA
run_cols = ['Player', 'Run_TD', 'Run_OnePointConversion', 'Run_TwoPointConversion']
run_df = stat_df.filter(items=run_cols).groupby('Player').sum(numeric_only=True)
run_df = run_df.sort_values(by='Run_TD', ascending=False)
run_df.columns = ['TD', '1 Point Conversions', '2 Point Conversions']

# END OF RUSHING DATA

# DEFENSIVE DATA
def_cols = ['Player', 'Def_Flag', 'Def_INT', 'Def_TD']
def_df = stat_df.filter(items=def_cols).groupby('Player').sum(numeric_only=True)
def_df = def_df.sort_values(by='Def_Flag', ascending=False)
def_df.columns = ['Flags', 'Interceptions', 'TD']

# END OF DEFENSIVE DATA

# Kick Return
kr_cols = ['Player', 'KR_TD']
kr_df = stat_df.filter(items=kr_cols).groupby('Player').sum(numeric_only=True)
kr_df = kr_df.sort_values(by='KR_TD', ascending=False)
kr_df.columns = ['TD']

# Streamlit App
st.title("GWW Jr Girls Flag Football 2025")

st.write("Passing Stats")
st.write(pass_df)

st.write("Rushing Stats")
st.write(run_df)

st.write("Receiving Stats")
st.write(rec_df)

st.write("Defensive Stats")
st.write(def_df)

st.write("Kick Return")
st.write(kr_df)