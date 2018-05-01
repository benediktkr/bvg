#!/usr/bin/env python3

import argparse
import logging
import pprint

import bvg
from config import config

parser = argparse.ArgumentParser(description='Search for BVG station')
parser.add_argument("searchterm", type=str, default="", help="Station name", nargs="?")
parser.add_argument("--fuzzy", action="store_true", help="Use fuzzy search")
parser.add_argument("--debug", action="store_true", help="Print full JSON")
args = parser.parse_args()

l = logging.getLogger(__name__)

def main():
    l.info("Using config: {}".format(bvg.CONFIGFILE))
    if not args.searchterm:
        searchterm = input("Search for station: ")
    else:
        searchterm = args.searchterm

    stations = bvg.search_station(searchterm, args.fuzzy)
    for (i, station) in enumerate(stations):
        print(f'{i}. {station["name"]}')

    choice = int(input("Choice: "))
    l.info(f'Added station id {stations[choice]["id"]} to config')
    config['stations'].append({
        'name': stations[choice]['name'],
        'id': stations[choice]['id']
    })

    if args.debug:
        pprint.pprint(stations[choice])
    config.save()

if __name__ == "__main__":
    main()
