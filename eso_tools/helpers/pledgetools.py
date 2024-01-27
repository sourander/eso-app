
import yaml
import datetime
import numpy as np

from datetime import date
from eso_tools.models.pledges import PledgeList


def offset_pledge_list_to_today(dungeons, ref_date_dungeon, reference_date, today):
    """Offsets all pledge lists so that the 0th element is today's dungeon.
    """
    # Find out the index of reference date's dungeon
    # This will be the starting point for the offset
    offset_ref = dungeons.index(ref_date_dungeon)

    # How many days have passed since reference date?
    # This will be added to the offset
    delta = (today - reference_date).days
    offset_days = (delta % len(dungeons))

    # Add and reverse direction
    offset = (offset_ref + offset_days) * -1

    dungeons_from_today = list(np.roll(dungeons,  offset))

    return dungeons_from_today

def load_config(config_path):
    """
    Loads the configuration file.
    """

    # Load the configuration file
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Get the reference date in format yyyy/m/d
    return config


def pledges_reordered_from_today(config:dict, today:datetime.date) -> list[PledgeList]:

    difficulties = config["difficulties"].keys()
    reference_date = datetime.datetime.fromisoformat(config["reference_date"]).date()

    pledges = []

    for difficulty in config["difficulties"]:
        # Config
        giver = config["difficulties"][difficulty]["giver"]
        ref_date_pledge = config["difficulties"][difficulty]["reference"]
        dungeons = config["difficulties"][difficulty]["dungeons"]

        # Offset the dungeons to today. 0th element is today's dungeon
        dungeons = offset_pledge_list_to_today(dungeons, ref_date_pledge, reference_date, today)
        new = PledgeList(giver=giver, dungeons=dungeons)
        pledges.append(new)

    return pledges