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
    "hinterlands": "hinterlands-2.yaml",
    "empires": "empires.yaml"
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

'''
(OLD TO BE DELETED)
sets = {}
for k, v in ARGUMENT_NAME_TO_YAML_SET.items():
    set_filepath = pathlib.Path.cwd() / "sets" / v
    with open(set_filepath, 'r') as file:
        sets[k] = yaml.safe_load(file)
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
    parser.add_argument('--hinterlands', type=int, help='COMING SOON')
    parser.add_argument('--empires', type=int, help='COMING SOON')
    args = parser.parse_args()

    """
    TODO: nest in "kingdom" and "landscape"
    TODO: the results
    KINGDOM CARDS
    For each set, select the # of cards as defined by the argument value
    Resulting data will be in the results dict (titled sets), of cardname -> set, such as:
        results = {
            'Militia': 'Base'
            'Shanty Town': 'Intrigue'
        }
    
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
    for setname in SETNAME_TO_YAMLNAME:
        # This is so we can get args.base, args.intrigue, etc... programatically
        set_num_kcards = getattr(args, setname)
        if set_num_kcards:
            # TODO New way
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


            '''
            (OLD WAY)
            # Argument for this set was provided with a non-zero number, so lets pick some cards!
            picked_cards = random.sample(sets[setname]["cards"], set_num_cards)
            for card in picked_cards:
                # Adding just the basic card info into results dict
                results[card["name"]] = setname.title()
            '''

    console.print(pickedpiles)
    console.print(randpile)
    sys.exit()    


    console.print(Panel.fit("Picked Cards"))
    # TODO: COLOR based on victory/treasure, etc
    n = 1
    for res_card, res_set in results.items():
        # <3 and <20 for spacing. Num has to be combined with . old fashioned way for this to work
        console.print(f"{str(n) + '.' : <3} {res_card : <20} ({res_set})")
        n += 1


    console.print(Panel.fit("Copy/Paste Format for Online"))
    comstring = ''
    for res_card in results:
        if not comstring:
            # If first entry, don't add comma
            comstring = f"{res_card}"
        else:
            comstring += f", {res_card}"
    console.print(comstring)

    




if __name__ == "__main__":
    main(sys.argv[1:])