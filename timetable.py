#!/usr/bin/env python3

import logging
from pprint import pprint
import argparse
from datetime import datetime, timedelta

from dateutil.parser import parse as dateparse
import bvg
from config import config

parser = argparse.ArgumentParser("Print timetable for stations")
parser.add_argument("--all", action="store_true", help="Show all lines")
parser.add_argument("--debug", action="store_true", help="Print JSON for departures")
args = parser.parse_args()


# fix this
def trim_station(station):
    prefixes = ["S+U", "S", "U"]
    for prefix in prefixes:
        if station.startswith(prefix):
            return station[len(prefix)+1:]
    return station

def trim_line(line):
    prefixes = ["Tram ", "Bus "]

    for prefix in prefixes:
        if line.startswith(prefix):
            return line[len(prefix)+1:]
    return line

def main():
    for station in config['stations']:
        print(f' - {station["name"]}')
        departures = bvg.get_station_departures(station["id"])
        #pprint([a['delay'] for a in departures])
        for departure in departures:
            line = departure['line']['name']
            if not args.all and line not in config['lines']:
                continue

            line = line.rjust(8)

            direction = trim_station(departure['direction']).ljust(33)

            # Other interesting fields:
            # journeyId
            # remarks

            # Needs to be set, otherwise the format string uses "Cancelled"
            status = ""

            if departure.get('cancelled', False) == True:
                status = "Cancelled"
            else:

                delay = int(departure['delay'] or 0) // 60 # minutes
                # Naively cutting the timezone off the string
                when = dateparse(departure['when'][:-6])
                if when > datetime.now():
                    wait = when - datetime.now()
                    minutes = wait.seconds // 60;
                    if delay > 0:
                        status = f'{minutes} min (+{delay}m)'
                    else:
                        status = f'{minutes} min'

                    if args.debug:
                        pprint(departure)
                    print(f'  {line} | {direction} | {status}')


if __name__ == "__main__":
    main()
