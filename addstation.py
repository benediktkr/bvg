#!/usr/bin/env python3

import argparse
import configparser
import logging
import pprint

import bvg
from config import config

parser = argparse.ArgumentParser(description='Search for BVG station')
parser.add_argument("searchterm", type=str, default="", help="Station name", nargs="?")
parser.add_argument("fuzzy", action="store_true", help="Use fuzzy search")
args = parser.parse_args()

if __name__ == "__main__":
    logging.info("Using config: {}".format(bvg.CONFIGFILE))
    if not args.searchterm:
        searchterm = input("Search for station: ")
    else:
        searchterm = args.searchterm

    stations = bvg.search_station(searchterm, args.fuzzy)
    for (i, station) in enumerate(stations):
        print(f'{i}. {station["name"]}')

    choice = int(input("Choice: "))
    print(stations[choice]["name"])
    print(stations[choice]["id"])
    config['stations'].append({
        'name': stations[choice]['name'],
        'id': stations[choice]['id']
    })

    config.save()


