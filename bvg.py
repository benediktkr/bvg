#!/usr/bin/env python3

import logging
import sys
from pprint import pprint
from datetime import datetime, timedelta
import argparse

from dateutil.parser import parse as dateparse
import requests

from config import config

XIdentifier = "https://github.com/benediktkr/bvg"
API = "https://2.vbb.transport.rest"
CONFIGFILE="bvg.ini"

parser = argparse.ArgumentParser(description='Search for BVG station')
parser.add_argument("--debug", action="store_true", help="Print full JSON")
args = parser.parse_args()

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
l = logging.getLogger(__name__)

def request(url, params=None):
    if not url.startswith("/"):
        raise ValueError("API endpoint must start with /")
    r = requests.get(API + url, params=params)
    headers = {
        'X-Identifier': XIdentifier,
        'Content-Type': 'application/json',
    }
    r.raise_for_status()
    return r.json()

def search_station(name, fuzzy=False):
    params = {
        'query': name,
        'fuzzy': fuzzy
    }
    return request("/stations", params)

def get_station(s_id):
    return request(f'/stations/{s_id}')

def get_station_departures(s_id):
    return request(f'/stations/{s_id}/departures')

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
        departures = get_station_departures(station["id"])
        #pprint([a['delay'] for a in departures])
        for departure in departures:
            if args.debug:
                pprint(departure)
            line = departure['line']['name'].rjust(8)
            direction = trim_station(departure['direction']).ljust(33)

            # Other interesting fields:
            # journeyId
            # remarks

            # Needs to be set, otherwise the format string uses "Cancelled"
            status = ""
            
            if departure.get('cancelled', False) == True:
                status = "Cancelled"
            else:

                delay = int(departure['delay']) # seconds
                # Naively cutting the timezone off the string
                when = dateparse(departure['when'][:-6])
                if when > datetime.now():
                    wait = when - datetime.now()
                    minutes = wait.seconds // 60;
                    status = f'{minutes} min'

            print(f'  {line} | {direction} | {status}')
            

if __name__ == "__main__":
    main()
