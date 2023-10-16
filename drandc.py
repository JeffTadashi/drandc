#!/usr/bin/env python3

import argparse
import pathlib
import random
from rich.console import Console
from rich.panel import Panel
import yaml
import sys

console = Console()

# This is also used as master list of all setnames themselves (which lines up to arguments)
SETNAME_TO_YAMLNAME = {
    "base": "base-set-2.yaml",
    "intrigue": "intrigue-2.yaml",
    "seaside": "seaside-2.yaml",
    "alchemy": "alchemy.yaml",
    "prosperity": "prosperity-2.yaml",
    "cornucopia": "cornucopia.yaml",
    "hinterlands": "hinterlands-2.yaml",
    "dark_ages": "dark-ages.yaml",
    "guilds": "guilds.yaml",
    "adventures": "adventures.yaml",
    "empires": "empires.yaml",
    "nocturne": "nocturne.yaml",
    "renaissance": "renaissance.yaml",
    "menagerie": "menagerie.yaml",
    "allies": "allies.yaml",
    "plunder": "plunder.yaml",
    "promos": "promos.yaml"
    }


# Create master card-like-things dict
'''
Create Randomizer Piles (one for Kingdom, one for Landscape)
kingdoms:
   [list of cards] - card has key/value of set
landscapes:
   [list of landscapes] - card has key/value of set, and key/value of the type of landscape

This list will be modified/deleted to track what cards were taken. Those cards will be "moved" to results.
'''
randpile = {
    "kingdoms": [],
    "landscapes": []
}
for setname, yamlname in SETNAME_TO_YAMLNAME.items():
    set_filepath = pathlib.Path.cwd() / "sets" / yamlname
    with open(set_filepath, 'r') as file:
        set = yaml.safe_load(file)
    # Iterate over each kingdom card, and copy into randpile while adding key/value for the set name itself
    for kcard in set["cards"]:
        kcard["set"] = setname
        randpile["kingdoms"].append(kcard)
    # Iterate over each landscape card type, and copy into randpile while adding key/value 
    # for the set name itself, and the key/value of the landscape type
    if 'events' in set:
        for landscape in set["events"]:
            landscape["set"] = setname
            landscape["type"] = "event"
            randpile["landscapes"].append(landscape)
    # TODO for landmarks, ways, projects






def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('-k','--kingdom', type=int, help='COMING SOON') ##TODO: these have to be picked last
    parser.add_argument('-b','--base', type=int, help='COMING SOON')
    parser.add_argument('--intrigue', type=int, help='COMING SOON')
    parser.add_argument('--seaside', type=int, help='COMING SOON')
    parser.add_argument('--alchemy', type=int, help='COMING SOON')
    parser.add_argument('--prosperity', type=int, help='COMING SOON')
    parser.add_argument('--cornucopia', type=int, help='COMING SOON')
    parser.add_argument('--hinterlands', type=int, help='COMING SOON')
    parser.add_argument('--dark-ages', type=int, help='COMING SOON')
    parser.add_argument('--guilds', type=int, help='COMING SOON')
    parser.add_argument('--adventures', type=int, help='COMING SOON')
    parser.add_argument('--empires', type=int, help='COMING SOON')
    parser.add_argument('--nocturne', type=int, help='COMING SOON')
    parser.add_argument('--renaissance', type=int, help='COMING SOON')
    parser.add_argument('--menagerie', type=int, help='COMING SOON')
    parser.add_argument('--allies', type=int, help='COMING SOON')
    parser.add_argument('--plunder', type=int, help='COMING SOON')
    parser.add_argument('--promos', type=int, help='COMING SOON')
    parser.add_argument('-e', '--event', type=int, help='COMING SOON') #TODO
    parser.add_argument('--event-adventures', type=int, help='COMING SOON')
    parser.add_argument('--event-empires', type=int, help='COMING SOON')
    parser.add_argument('--event-menagerie', type=int, help='COMING SOON')
    parser.add_argument('--event-plunder', type=int, help='COMING SOON')
    args = parser.parse_args()



    #################################
    # PICK THE CARDS
    #################################
    """
    GET KINGDOM AND LANDSCAPES!

    PICKED PILES: NEW WAY:
        results = {
            kingdoms:
            landscapes:
        }
    """
    pickedpiles = {
        "kingdoms": [],
        "landscapes": []
    }
    # PICK SET-SPECIFIC KINGDOM CARDS
    for setname in SETNAME_TO_YAMLNAME:
        # This is so we can get args.base, args.intrigue, etc... programatically
        set_num_kcards = getattr(args, setname)
        if set_num_kcards:
            # First, make sub-list of kcards that matches this set
            sublist = []
            for kcard in randpile["kingdoms"]:
                if kcard["set"] == setname:
                    sublist.append(kcard)
            # Next, pick the total random cards needed from this sublist
            picked_kcards = random.sample(sublist, set_num_kcards)
            # Put these kcards into the pickedpiles, and remove from randpiles
            for kcard in picked_kcards:
                pickedpiles["kingdoms"].append(kcard)
                randpile["kingdoms"].remove(kcard)
    # PICK ANY KINGDOM CARDS (TODO)

    # PICK SET-SPECIFIC EVENTS
    for setname in SETNAME_TO_YAMLNAME:
        # Check if attribute of events_setname exists (from arguments)
        if hasattr(args, f'event_{setname}'):
            # Now we can check if the attribute has a non-zero value
            set_num_events = getattr(args, f'event_{setname}')
            if set_num_events:
                # First, make sub-list of landscapes that matches this set and type
                sublist = []
                for landscape in randpile["landscapes"]:
                    if landscape["set"] == setname and landscape["type"] == "event":
                        sublist.append(landscape)
                # Next, pick the total random landscapes needed from this sublist
                picked_landscapes = random.sample(sublist, set_num_events)
                # Put these landscapes into the pickedpiles, and remove from randpiles
                for landscape in picked_landscapes:
                    pickedpiles["landscapes"].append(landscape)
                    randpile["landscapes"].remove(landscape)       



    #################################
    # PRINTING RESULTS
    #################################


    console.print(Panel.fit("Picked Cards"))
    # TODO: COLOR based on victory/treasure, etc
    console.print("")
    console.print("        ─━═Kingdom Cards═━─        ", style='bold cyan')
    n = 1
    for kcard in pickedpiles["kingdoms"]:
        # <3 and <20 for spacing. Num has to be combined with . old fashioned way for this to work
        console.print(f"{str(n) + '.' : <3} {kcard['name'] : <27} ({kcard['set'].title()})")
        n += 1
    console.print("")


    console.print("")
    console.print("        ─━═Landscapes═━─        ", style='bold cyan')
    n = 1
    for landscape in pickedpiles["landscapes"]:
        # <3 and <20 for spacing. Num has to be combined with . old fashioned way for this to work
        console.print(f"{str(n) + '.' : <3} {landscape['name'] : <27} ({landscape['set'].title()})")
        n += 1
    console.print("")


    console.print(Panel.fit("Copy/Paste Format for Online"))
    comstring = ''
    for kcard in pickedpiles["kingdoms"]:
        if not comstring:
            # If first entry, don't add comma
            comstring = f"{kcard['name']}"
        else:
            comstring += f", {kcard['name']}"
    console.print(comstring)
    # TODO Landscapes to this
    




if __name__ == "__main__":
    main(sys.argv[1:])