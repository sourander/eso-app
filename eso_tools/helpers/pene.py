import streamlit as st

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
        st.subheader("The tank")

        add_basic_checkbox_buff(buffs, "Major Breach", MAJOR_BREACH)
        add_basic_checkbox_buff(buffs, "Minor Breach", MINOR_BREACH)
        add_basic_checkbox_buff(buffs, "Arcanist Tank (Runic Sunder)", RUNIC_SUNDER, default=False)
        add_basic_checkbox_buff(buffs, "Crusher Enchant (Infused)", CRUSHER_INFUSED)
        # add_basic_checkbox_buff(buffs, "Tremorscale", TREMORSCALE, default=False)

        if st.checkbox("Tremorscale", value=False):
            n = st.slider("Tank resistance:", min_value=30000, max_value=35000, value=33000, step=100)
            slope = 0.079998
            bias = -58.69
            buffs.append(
                PenetrationBuff(
                    name =f"Tremorscale ({n / 1000}k resistance)",
                    penetration = int(n * slope + bias),
                )
            )

        st.subheader("Other DDs")

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

        add_basic_checkbox_buff(buffs, "You are a Bosmer (Wood Elf)", 950, default=False)
        add_basic_checkbox_buff(
            buffs, "You are a Nightblade and flanking", 2974, default=False
        )
        add_basic_checkbox_buff(
            buffs, "You have a Necro Grave Lord ability slotted", 1500, default=False
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
    st.divider()
    st.subheader("Typical set pieces with penetration")
    st.write("""
        Many sets have a typical 1-piece bonus being 1487 penetration. These sets include e.g. Tzogvin,
        Kra'gh, Ansuul, Runecarver, and many others.
        How many of these set bonuses are you wearing?
    
    """)
    n = st.slider("Penetration bonuses", 0, 5, 0)
    penetration_buffs.append(
        PenetrationBuff(
            name=f"Typical set ({n} bonuses)",
            penetration=1487 * n,
        )
    )

    st.divider()

    st.subheader("Any special sets with penetration?")
    selected_sets = st.multiselect("Sets worn", list(SET_OPTIONS.keys()), max_selections=3)
    # Calculate penetration from selected sets
    for set_name in selected_sets:
        if set_name in SET_OPTIONS:
            set_penetration = SET_OPTIONS[set_name]
            penetration_buffs.append(
                PenetrationBuff(name=set_name, penetration=set_penetration)
            )

    return penetration_buffs


def append_light_armor_buffs(penetration_buffs: list[PenetrationBuff]):
    st.divider()
    st.subheader("Light Armor Pieces")
    n = st.slider("# Light Armor Pieces", min_value=0, max_value=7, value=1, step=1)

    # Calculate penetration from light armor pieces
    light_armor_penetration = n * LIGHT_ARMOR_PASSIVE
    penetration_buffs.append(
        PenetrationBuff(
            name=f"{n} Light Armor Pieces", penetration=light_armor_penetration
        )
    )

    return penetration_buffs