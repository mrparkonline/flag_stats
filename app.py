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

game_sheet = stat_sheet.get_worksheet(1)
game_df = pd.DataFrame(game_sheet.get_all_records())
game_df.columns = ['Game Date', 'GWW Score', 'Opponent Score', 'Opposing Team', 'Game Result', 'Type of Game']

st.set_page_config(
    page_title="JR Flag Stats",
    page_icon=":football:",
    layout="wide"
)
# End of Initialzations

# PASSING DATA
passing_cols = ['Player', 'Passing_TD', 'Passing_OnePointConversion', 'Passing_TwoPointConversion']
pass_df = stat_df.filter(items=passing_cols).groupby('Player').sum(numeric_only=True)

pass_df = pass_df[(pass_df.T != 0).any()]

pass_df = pass_df.sort_values(by='Passing_TD', ascending=False)
pass_df.columns = ['TD', '1 Point Conversions', '2 Point Conversions']

# END OF PASSING DATA

# RECEIVING DATA
rec_cols = ['Player', 'Receiving_Catches', 'Receiving_TD', 'Receiving_OnePointConversion', 'Receiving_TwoPointConversion']
rec_df = stat_df.filter(items=rec_cols).groupby('Player').sum(numeric_only=True)

rec_df = rec_df[(rec_df.T != 0).any()]

rec_df = rec_df.sort_values(by='Receiving_Catches', ascending=False)
rec_df.columns = ['Receptions', 'TD', '1 Point Conversions', '2 Point Conversions']

# END OF RECEIVING DATA

# RUSHING DATA
run_cols = ['Player', 'Run_TD', 'Run_OnePointConversion', 'Run_TwoPointConversion']
run_df = stat_df.filter(items=run_cols).groupby('Player').sum(numeric_only=True)

run_df = run_df[(run_df.T != 0).any()]

run_df = run_df.sort_values(by='Run_TD', ascending=False)
run_df.columns = ['TD', '1 Point Conversions', '2 Point Conversions']

# END OF RUSHING DATA

# DEFENSIVE DATA
def_cols = ['Player', 'Def_Flag', 'Def_INT', 'Def_TD']
def_df = stat_df.filter(items=def_cols).groupby('Player').sum(numeric_only=True)

def_df = def_df[(def_df.T != 0).any()]

def_df = def_df.sort_values(by='Def_Flag', ascending=False)
def_df.columns = ['Flags', 'Interceptions', 'TD']

# END OF DEFENSIVE DATA

# Kick Return
kr_cols = ['Player', 'KR_TD']
kr_df = stat_df.filter(items=kr_cols).groupby('Player').sum(numeric_only=True)

kr_df = kr_df[(kr_df.T != 0).any()]

kr_df = kr_df.sort_values(by='KR_TD', ascending=False)
kr_df.columns = ['TD']

# Streamlit App
st.header("GWW Flag Football Stats")
st.markdown("*Junior Girl's 2025 Season*")

st.markdown("**Passing Stats**")
st.write(pass_df)

st.markdown("**Rushing Stats**")
st.write(run_df)

st.markdown("**Receiving Stats**")
st.write(rec_df)

st.markdown("**Defensive Stats**")
st.write(def_df)

st.markdown("**Kick Return**")
st.write(kr_df)

with st.expander("Game Results"):
    st.write(game_df)