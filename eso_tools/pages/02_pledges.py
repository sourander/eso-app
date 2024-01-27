import streamlit as st
import datetime
import difflib

from eso_tools.helpers.pledgetools import *
import pandas as pd


def main():
    st.title("Pledges")
    config = load_config("eso_tools/config/pledges.yml")
    today = datetime.date.today()

    easy, mid, dlc = pledges_reordered_from_today(config, today)

    rows = []

    n_e, n_m, n_d = len(easy.dungeons), len(mid.dungeons), len(dlc.dungeons)
    n_total = sum([n_e, n_m, n_d])
    st.markdown(f"""
        As of now, there are total of {n_total} dungeons in ESO. 
        
        They are given by three pledge givers, each giving a different set of dungeons:
        
        * **{easy.giver}**: {n_e} dungeons, 
        * **{mid.giver}**: {n_m} dungeons, 
        * **{dlc.giver}**: {n_d} dungeons
    """)

    n = st.slider("How many days' pledges to show?", 0, 31, 3)
    
    for i in range(n_total):
        day = today + datetime.timedelta(days=i)
        row = {
            "day": day,
            "weekday": day.strftime("%A"),
            easy.giver: easy.dungeons[i % len(easy.dungeons)],
            mid.giver: mid.dungeons[i % len(mid.dungeons)],
            dlc.giver: dlc.dungeons[i % len(dlc.dungeons)],
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    st.write(df.head(n))

    st.divider()

    st.subheader("Search for the next time a given dungeon is a pledge:")
    
    # query = st.text_input("Dungeon name", "Fungal Grotto I")

    # if query:

    #     # Find similar items
    #     suggestions = difflib.get_close_matches(query, easy.dungeons + mid.dungeons + dlc.dungeons)

    # Multichoise selector
    selected = st.multiselect("Select dungeon", easy.dungeons + mid.dungeons + dlc.dungeons, max_selections=5)

    if selected:

        # Filter rows based on substring in any of the specified columns
        filtered_rows = df[
            (df[easy.giver].astype(str) == selected[0]) |
            (df[mid.giver].astype(str) == selected[0]) |
            (df[dlc.giver].astype(str) == selected[0])
        ]

        # First date
        dungeon_date = filtered_rows.iloc[0]["day"]

        st.metric(
            "Next time this dungeon is a pledge:",
            str(dungeon_date),
            delta=str((dungeon_date - today).days) + " days",
            delta_color="normal",
            help=None,
            label_visibility="visible",)
        



if __name__ == "__main__":
    main()

