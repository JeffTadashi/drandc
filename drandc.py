#!/usr/bin/env python3

# TODO: print inputs in "english"
# TODO: print fun fact: how many combinations were possible on this choice
# TODO: copy to clipboard automatically with https://github.com/asweigart/pyperclip

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

# This is needed to iterate over landscape types
# Notably, the YAML files use "events" whereas this script will use "event", etc
LANDSCAPE_NAMES_TO_NAME = {
    "events": "event",
    "landmarks": "landmark", 
    "projects": "project", 
    "ways": "way", 
    "traits": "trait"
}



# Create master randomizer piles
'''
Create Randomizer Piles (one for Kingdom, one for Landscape)
kingdoms:
   [list of cards as dicts] - card has additional key/value of set
landscapes:
   [list of landscapes as dicts] - card has additional key/value of set, and additional key/value of the type of landscape

This list will be modified/deleted to track what cards were taken. Those cards will be "moved" to pickedpiles.
'''
randpiles = { 
    "kingdoms": [],
    "landscapes": []
}
for setname, yamlname in SETNAME_TO_YAMLNAME.items():
    set_filepath = pathlib.Path.cwd() / "sets" / yamlname
    with open(set_filepath, 'r') as file:
        set = yaml.safe_load(file)
    # Iterate over each kingdom card, and copy into randpiles while adding key/value for the set name itself
    for kcard in set["cards"]:
        kcard["set"] = setname
        randpiles["kingdoms"].append(kcard)
    # Iterate over each landscape card type, and copy into randpiles while adding key/value 
    # for the set name itself, and the key/value of the landscape type
    for name_p, name_s in LANDSCAPE_NAMES_TO_NAME.items():
        if name_p in set:
            for landscape in set[name_p]:
                landscape["set"] = setname
                landscape["type"] = name_s
                randpiles["landscapes"].append(landscape)



banner_1 = r'''
______                     _ _____ 
|  _  \                   | /  __ \
| | | |_ __ __ _ _ __   __| | /  \/
| | | | '__/ _` | '_ \ / _` | |    
| |/ /| | | (_| | | | | (_| | \__/\
|___/ |_|  \__,_|_| |_|\__,_|\____/
'''
banner_2 = '''
    by JeffTadashi
   version 0.1
  https://github.com/JeffTadashi/drandc

'''


def main(argv):

    console.print(banner_1, style='bold', highlight=False)
    console.print(banner_2)

    parser = argparse.ArgumentParser()
    parser.add_argument('-k','--kingdom', type=int, help='# of kingdom cards from any/all sets')
    parser.add_argument('-b','--base', type=int, help='# of kingdom cards from Dominion Base (2nd Edition)')
    parser.add_argument('--intrigue', type=int, help='# of kingdom cards from Intrigue (2nd Edition)')
    parser.add_argument('--seaside', type=int, help='# of kingdom cards from Seaside (2nd Edition)')
    parser.add_argument('--alchemy', type=int, help='# of kingdom cards from Alchemy')
    parser.add_argument('--prosperity', type=int, help='# of kingdom cards from Prosperity (2nd Edition)')
    parser.add_argument('--cornucopia', type=int, help='# of kingdom cards from Cornucopia')
    parser.add_argument('--hinterlands', type=int, help='# of kingdom cards from Hinterlands (2nd Edition)')
    parser.add_argument('--dark-ages', type=int, help='# of kingdom cards from Dark Ages')
    parser.add_argument('--guilds', type=int, help='# of kingdom cards from Guilds')
    parser.add_argument('--adventures', type=int, help='# of kingdom cards from Adventures')
    parser.add_argument('--empires', type=int, help='# of kingdom cards from Empires')
    parser.add_argument('--nocturne', type=int, help='# of kingdom cards from Nocturne')
    parser.add_argument('--renaissance', type=int, help='# of kingdom cards from Renaissance')
    parser.add_argument('--menagerie', type=int, help='# of kingdom cards from Menagerie')
    parser.add_argument('--allies', type=int, help='# of kingdom cards from Allies')
    parser.add_argument('--plunder', type=int, help='# of kingdom cards from Plunder')
    parser.add_argument('--promos', type=int, help='# of kingdom cards from Promos')
    parser.add_argument('-l', '--landscape', type=int, help='# of landscapes from any/all sets')
    parser.add_argument('-e', '--event', type=int, help='# of events from any/all sets')
    parser.add_argument('--event-adventures', type=int, help='# of events from Adventures')
    parser.add_argument('--event-empires', type=int, help='# of events from Empires')
    parser.add_argument('--event-menagerie', type=int, help='# of events from Menagerie')
    parser.add_argument('--event-plunder', type=int, help='# of events from Plunder')
    parser.add_argument('--landmark', type=int, help='# of landmarks (exclusive to Empires)')
    parser.add_argument('--project', type=int, help='# of projects (exclusive to Renaissance)')
    parser.add_argument('--way', type=int, help='# of ways (exclusive to Menagerie)')
    parser.add_argument('--trait', type=int, help='# of traits (exclusive to Plunder)')
    parser.add_argument('-s', '--set', type=int, help='Simple # of sets picked randomly. Using this overrides all kingdom/landmark operations')
    args = parser.parse_args()


    #################################
    # SIMPLE PICK THE SET (IF USING)
    #################################
    if args.set:
        picked_sets = random.sample(sorted(SETNAME_TO_YAMLNAME), args.set)
        console.print(Panel.fit("Picked Sets"), style='bold')
        n = 1
        for setname in picked_sets:
            # <3 for spacing. Num has to be combined with . old fashioned way for this to work
            console.print(f"{str(n) + '.' : <3} {setname.title()} ")
            n += 1
        # Exiting, as all other arguments are ignored
        sys.exit()

    #################################
    # PICK THE CARDS
    #################################
    """
    GET KINGDOM AND LANDSCAPES!
    
    Main data piece:
        pickedpiles = {
            kingdoms: [each card (as dict)]
            landscapes: [each landscape (as dict)]
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
            for kcard in randpiles["kingdoms"]:
                if kcard["set"] == setname:
                    sublist.append(kcard)
            # Next, pick the total random cards needed from this sublist
            picked_kcards = random.sample(sublist, set_num_kcards)
            # Put these kcards into the pickedpiles, and remove from randpiles
            for kcard in picked_kcards:
                pickedpiles["kingdoms"].append(kcard)
                randpiles["kingdoms"].remove(kcard)

    # PICK ANY KINGDOM CARDS
    num_kcards = getattr(args, "kingdom")
    if num_kcards:
        # Next, pick the total random kcards needed from the remaining randpile
        picked_kcards = random.sample(randpiles["kingdoms"], num_kcards)
        # Put these kcards into the pickedpiles, and remove from randpiles
        for kcard in picked_kcards:
            pickedpiles["kingdoms"].append(kcard)
            randpiles["kingdoms"].remove(kcard)

    # PICK SET-SPECIFIC EVENTS
    for setname in SETNAME_TO_YAMLNAME:
        # Check if attribute of events_setname exists (from arguments)
        if hasattr(args, f'event_{setname}'):
            # Now we can check if the attribute has a non-zero value
            set_num_events = getattr(args, f'event_{setname}')
            if set_num_events:
                # First, make sub-list of landscapes that matches this set and type
                sublist = []
                for landscape in randpiles["landscapes"]:
                    if landscape["set"] == setname and landscape["type"] == "event":
                        sublist.append(landscape)
                # Next, pick the total random landscapes needed from this sublist
                picked_landscapes = random.sample(sublist, set_num_events)
                # Put these landscapes into the pickedpiles, and remove from randpiles
                for landscape in picked_landscapes:
                    pickedpiles["landscapes"].append(landscape)
                    randpiles["landscapes"].remove(landscape)
    
    # PICK ANY EVENTS
    # Check if the "plain" event attribute is non-zero
    num_events = getattr(args, 'event')
    if num_events:
        # First, make sub-list of landscapes that matches this type
        sublist = []
        for landscape in randpiles["landscapes"]:
            if landscape["type"] == "event":
                sublist.append(landscape)
        # Next, pick the total random landscapes needed from this sublist
        picked_landscapes = random.sample(sublist, num_events)
        # Put these landscapes into the pickedpiles, and remove from randpiles
        for landscape in picked_landscapes:
            pickedpiles["landscapes"].append(landscape)
            randpiles["landscapes"].remove(landscape)   

    # PICK LANDMARKS
    # (Note: only in Empires)
    # Check if the landmark attribute is non-zero
    num_landmarks = getattr(args, 'landmark')
    if num_landmarks:
        # First, make sub-list of landscapes that matches this type
        sublist = []
        for landscape in randpiles["landscapes"]:
            if landscape["type"] == "landmark":
                sublist.append(landscape)
        # Next, pick the total random landscapes needed from this sublist
        picked_landscapes = random.sample(sublist, num_landmarks)
        # Put these landscapes into the pickedpiles, and remove from randpiles
        for landscape in picked_landscapes:
            pickedpiles["landscapes"].append(landscape)
            randpiles["landscapes"].remove(landscape)

    # PICK PROJECTS
    # (Note: only in Renaissance)
    # Check if the project attribute is non-zero
    num_projects = getattr(args, 'project')
    if num_projects:
        # First, make sub-list of landscapes that matches this type
        sublist = []
        for landscape in randpiles["landscapes"]:
            if landscape["type"] == "project":
                sublist.append(landscape)
        # Next, pick the total random landscapes needed from this sublist
        picked_landscapes = random.sample(sublist, num_projects)
        # Put these landscapes into the pickedpiles, and remove from randpiles
        for landscape in picked_landscapes:
            pickedpiles["landscapes"].append(landscape)
            randpiles["landscapes"].remove(landscape)

    # PICK WAYS
    # (Note: only in Menagerie)
    # Check if the way attribute is non-zero
    num_ways = getattr(args, 'way')
    if num_ways:
        # First, make sub-list of landscapes that matches this type
        sublist = []
        for landscape in randpiles["landscapes"]:
            if landscape["type"] == "way":
                sublist.append(landscape)
        # Next, pick the total random landscapes needed from this sublist
        picked_landscapes = random.sample(sublist, num_ways)
        # Put these landscapes into the pickedpiles, and remove from randpiles
        for landscape in picked_landscapes:
            pickedpiles["landscapes"].append(landscape)
            randpiles["landscapes"].remove(landscape)

    # PICK TRAITS
    # (Note: only in Plunder)
    # Check if the trait attribute is non-zero
    num_traits = getattr(args, 'trait')
    if num_traits:
        # First, make sub-list of landscapes that matches this type
        sublist = []
        for landscape in randpiles["landscapes"]:
            if landscape["type"] == "trait":
                sublist.append(landscape)
        # Next, pick the total random landscapes needed from this sublist
        picked_landscapes = random.sample(sublist, num_traits)
        # Put these landscapes into the pickedpiles, and remove from randpiles
        for landscape in picked_landscapes:
            pickedpiles["landscapes"].append(landscape)
            randpiles["landscapes"].remove(landscape)

    # PICK ANY LANDSCAPE
    num_landscapes = getattr(args, "landscape")
    if num_landscapes:
        # Next, pick the total random landscapes needed from the remaining randpile
        picked_landscapes = random.sample(randpiles["landscapes"], num_landscapes)
        # Put these landscapes into the pickedpiles, and remove from randpiles
        for landscape in picked_landscapes:
            pickedpiles["landscapes"].append(landscape)
            randpiles["landscapes"].remove(landscape)


    #################################
    # PRINTING RESULTS
    #################################

    console.print(Panel.fit("Picked Cards"), style='bold')
    console.print("")
    console.print("        ─━═Kingdom Cards═━─        ", style='bold cyan')
    n = 1
    for kcard in pickedpiles["kingdoms"]:
        # Set color. For multi-types, the first chosen here is the priority color
        if kcard.get('isTreasure'): color = "yellow"
        elif kcard.get('isAttack'): color = "red"
        elif kcard.get('isReaction'): color = "cyan"
        elif kcard.get('isVictory'): color = "green"
        else: color = "white"
        # Manual exception: Harem now is known as Farm
        if kcard['name'] == 'Harem': kcard['name'] = 'Harem (Farm)'
        # <3 and <20 for spacing. Num has to be combined with . old fashioned way for this to work
        console.print(f"{str(n) + '.' : <3} [{color}]{kcard['name'] : <27}[/{color}] ({kcard['set'].title()})")
        n += 1


    console.print("")
    console.print("        ─━═Landscapes═━─        ", style='bold cyan')
    n = 1
    for landscape in pickedpiles["landscapes"]:
        # Set color, if a non-event landscape
        if landscape['type'] == 'landmark': color = "green"
        elif landscape['type'] == 'project': color = "red"
        elif landscape['type'] == 'way': color = "cyan"
        elif landscape['type'] == 'trait': color = "magenta"
        else: color = "white"
        # <3 and <27 for spacing. Num has to be combined with . old fashioned way for this to work
        console.print(f"{str(n) + '.' : <3} [{color}]{landscape['name'] : <27}[/{color}] ({landscape['set'].title()})")
        n += 1
    console.print("")



    console.print(Panel.fit("Copy/Paste Format for Online"), style='bold')
    comstring = ''
    for kcard in pickedpiles["kingdoms"]:
        # if kcard is split pile (e.g. "Gladiator / Fortune"), only use the first card name.
        # (This is the format online Dominion uses)
        if r"/" in kcard['name']:
            # Use partition to separate before "/" and after. 
            kcard['name'], unused_sep, unused_tail = kcard['name'].partition(r"/")
            # Remove extra space at end
            kcard['name'] = kcard['name'].strip()
        # Manual exception: Harem now is known as Farm
        if 'Harem' in kcard['name']: kcard['name'] = 'Farm'
        if not comstring:
            # If first entry, don't add comma
            comstring = f"{kcard['name']}"
        else:
            comstring += f", {kcard['name']}"
    for landscape in pickedpiles["landscapes"]:
        if not comstring:
            # If first entry, don't add comma
            comstring = f"{landscape['name']}"
        else:
            comstring += f", {landscape['name']}"
    console.print(comstring)
    




if __name__ == "__main__":
    main(sys.argv[1:])