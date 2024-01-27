import streamlit as st
import pandas as pd

from eso_tools.models.penetration import PenetrationBuff
from eso_tools.config.pene_const import *
from eso_tools.helpers.pene import *


# Main Streamlit app
def main():
    st.title("Elder Scrolls Online Penetration Calculator")
    st.markdown(
        """
        This tool calculates the total penetration you have on a target. It is meant to be used for PvE content.
        Choose the modifiers from below. You can see the results by browsing down. The target is expected to have 18000 resistance.
    """
    )

    st.divider()

    # User inputs
    total_resistance = 18200

    penetration_buffs: list[PenetrationBuff] = []

    penetration_buffs = append_checkbox_buffs(penetration_buffs)
    penetration_buffs = append_set_buffs(penetration_buffs)
    penetration_buffs = append_light_armor_buffs(penetration_buffs)

    total_penetration = sum(x.penetration for x in penetration_buffs)
    remaining_resistance = total_resistance - total_penetration

    # Display total penetration

    st.divider()
    st.subheader("Results")
    st.metric(
        "⚔️ Total Penetration:",
        total_penetration,
        delta=-remaining_resistance,
        delta_color="normal",
        help=None,
        label_visibility="visible",
    )
    st.markdown(
        """    
        The large number is the total penetration you have. The small number is the remaining resistance of the target.
        Choose your penetration modifiers from the main site's checkboxes and other inputs.
    """
    )

    st.divider()

    # Display as DataFrame
    if st.checkbox("Show detailed values", value=False):
        st.subheader("Detailed values")
        buffs = [x.model_dump() for x in penetration_buffs]
        df = pd.DataFrame(buffs, columns=PenetrationBuff.model_fields.keys())
        df = df.sort_values(by=["penetration"], ascending=False)
        st.dataframe(df)


if __name__ == "__main__":
    main()
