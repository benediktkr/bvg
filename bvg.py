#!/usr/bin/env python3

import logging

import requests

XIdentifier = "https://github.com/benediktkr/bvg"
API = "https://2.vbb.transport.rest"

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
    return request(f'/stations/{s_id}', {'results': 20})

def get_station_departures(s_id):
    return request(f'/stations/{s_id}/departures')
