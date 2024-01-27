import streamlit as st
import pandas as pd

from eso_tools.models.penetration import PenetrationBuff
from eso_tools.config.pene_const import *


def add_basic_checkbox_buff(
    penetration_buffs: list[PenetrationBuff],
    name: str,
    penetration: int,
    default=True,
):
    if st.checkbox(name, value=default):
        penetration_buffs.append(PenetrationBuff(name=name, penetration=penetration))
    return penetration_buffs


def add_two_choice_checkbox_buff(
    penetration_buffs: list[PenetrationBuff],
    name: str,
    choice_question: str,
    choices: list[tuple[str, int]],
    default=True,
):
    if st.checkbox(name, value=default):
        radio = st.radio(choice_question, [choices[0][0], choices[1][0]])
        pen = choices[0][1] if radio == choices[0][0] else choices[1][1]
        penetration_buffs.append(PenetrationBuff(name=name, penetration=pen))
    return penetration_buffs


def append_checkbox_buffs(buffs: list[PenetrationBuff]):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Typical tank buffs")

        add_basic_checkbox_buff(buffs, "Major Breach", MAJOR_BREACH)
        add_basic_checkbox_buff(buffs, "Minor Breach", MINOR_BREACH)
        add_basic_checkbox_buff(buffs, "Arcanist Tank (Runic Sunder)", RUNIC_SUNDER)
        add_two_choice_checkbox_buff(
            buffs,
            "Crusher Enchant",
            "Type",
            [("Infused", 1638), ("Infused + Torug's Pact", 3276)],
        )
        add_basic_checkbox_buff(buffs, "Tremorscale", TREMORSCALE, default=False)

        st.subheader("Other")

        add_basic_checkbox_buff(buffs, "Alkosh", ALKOSH, default=False)
        add_basic_checkbox_buff(buffs, "Sorcerer (Crystal Weapon)", 1000, default=False)

    with col2:
        st.subheader("You")

        if st.checkbox("CP Passive", value=True):
            buffs.append(PenetrationBuff(name="CP Passive", penetration=CP_PASS))

        add_two_choice_checkbox_buff(
            buffs,
            "Sharpened trait",
            "Weapon Type",
            [("1H", SHARP_1H), ("2H", SHARP_2H)],
            default=False,
        )
        add_two_choice_checkbox_buff(
            buffs,
            "Mace or Maul",
            "Weapon Type",
            [("1H", MACE_1H), ("2H or 2*1H", MACE_2H)],
            default=False,
        )

        if st.checkbox("Lover Mundus", value=False):
            n = st.slider("# Divines", min_value=0, max_value=7, value=7, step=1)
            buffs.append(
                PenetrationBuff(
                    name=f"Lover Mundus ({n} Divines)",
                    penetration=2744 + n * 207,
                )
            )

        st.subheader("Your class or race")

        add_basic_checkbox_buff(buffs, "Bosmer race (Wood Elf)", 950, default=False)
        add_basic_checkbox_buff(
            buffs, "Nightblade flanking (Master assassin)", 2974, default=False
        )
        add_basic_checkbox_buff(
            buffs, "Necro Grave Lord ability (Dismember)", 1500, default=False
        )

        # Calculate penetration from light armor pieces
        if st.checkbox("You are an Arcanist", value=False):
            n = st.slider(
                "# Herald of the Tome abilities",
                min_value=0,
                max_value=6,
                value=1,
                step=1,
            )
            pen = n * 991
            buffs.append(
                PenetrationBuff(
                    name=f"{n} Herald of the Tome abilities", penetration=pen
                )
            )

    return buffs


def append_set_buffs(penetration_buffs: list[PenetrationBuff]):
    st.subheader("Sets")
    selected_sets = st.multiselect("Sets worn", list(SET_OPTIONS.keys()))

    # Calculate penetration from selected sets
    for set_name in selected_sets:
        if set_name in SET_OPTIONS:
            set_penetration = SET_OPTIONS[set_name]
            penetration_buffs.append(
                PenetrationBuff(name=set_name, penetration=set_penetration)
            )

    return penetration_buffs


def append_light_armor_buffs(penetration_buffs: list[PenetrationBuff]):
    st.subheader("Light Armor Pieces")
    n = st.slider("# Light Armor Pieces", min_value=0, max_value=7, value=1, step=1)

    # Calculate penetration from light armor pieces
    light_armor_penetration = n * 207
    penetration_buffs.append(
        PenetrationBuff(
            name=f"{n} Light Armor Pieces", penetration=light_armor_penetration
        )
    )

    return penetration_buffs


# Main Streamlit app
def main():
    st.title("Elder Scrolls Online Penetration Calculator")

    # User inputs
    total_resistance = st.number_input(
        "Target Resistance", min_value=0, value=18200, max_value=18200, step=100
    )

    penetration_buffs: list[PenetrationBuff] = []

    penetration_buffs = append_checkbox_buffs(penetration_buffs)
    penetration_buffs = append_set_buffs(penetration_buffs)
    penetration_buffs = append_light_armor_buffs(penetration_buffs)

    total_penetration = sum(x.penetration for x in penetration_buffs)
    remaining_resistance = total_resistance - total_penetration

    # Display total penetration

    st.divider()
    st.header("Results")
    st.write(
        "GUIDE: Choose all applicable penetration modifiers above. The total penetration can "
        "be seen below. The small number undernearth the value indicates the required penetration "
        "required to reach the cap if it is red. If it is green, you are over-penetrating."
    )
    st.metric(
        "⚔️ Total Penetration:",
        total_penetration,
        delta=-remaining_resistance,
        delta_color="normal",
        help=None,
        label_visibility="visible",
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
