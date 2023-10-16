#!/usr/bin/env python3

import argparse
import pathlib
import random
from rich.console import Console
from rich.panel import Panel
import yaml
import sys

console = Console()

ARGUMENT_NAME_TO_YAML_SET = {
    "base": "base-set-2.yaml",
    "intrigue": "intrigue-2.yaml",
    "hinterlands": "hinterlands-2.yaml"
    }


# Create master sets dict, and load each set (YAML) into this, nested by it's set name
sets = {}
for k, v in ARGUMENT_NAME_TO_YAML_SET.items():
    set_filepath = pathlib.Path.cwd() / "sets" / v
    with open(set_filepath, 'r') as file:
        sets[k] = yaml.safe_load(file)


def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('-k','--kingdom', type=int, help='COMING SOON')
    parser.add_argument('-b','--base', type=int, help='COMING SOON')
    parser.add_argument('--intrigue', type=int, help='COMING SOON')
    parser.add_argument('--hinterlands', type=int, help='COMING SOON')
    args = parser.parse_args()

    """
    KINGDOM CARDS
    For each set, select the # of cards as defined by the argument value
    Resulting data will be in the results dict (titled sets), of cardname -> set, such as:
        results = {
            'Militia': 'Base'
            'Shanty Town': 'Intrigue'
        }
    """
    results = {}
    for setname in ARGUMENT_NAME_TO_YAML_SET:
        # This is so we can get args.base, args.intrigue, etc... programatically
        set_num_cards = getattr(args, setname)
        if set_num_cards:
            # Argument for this set was provided with a non-zero number, so lets pick some cards!
            picked_cards = random.sample(sets[setname]["cards"], set_num_cards)
            for card in picked_cards:
                # Adding just the basic card info into results dict
                results[card["name"]] = setname.title()

    console.print(Panel.fit("Picked Cards"))
    n = 1
    for res_card, res_set in results.items():
        console.print(f"{n}. {res_card : <20} ({res_set})")
        n += 1



    




if __name__ == "__main__":
    main(sys.argv[1:])