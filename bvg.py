#!/usr/bin/env python3

import logging
import sys

import requests

XIdentifier = "https://github.com/benediktkr/bvg"
API = "https://2.vbb.transport.rest"
CONFIGFILE="bvg.ini"

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

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

