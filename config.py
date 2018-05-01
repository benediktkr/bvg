#!/usr/bin/env python3

import json
import logging

CONFIGFILE = "config.json"

TEMPLATE = {
    'stations': []
}

## MORALE WILL IMPROVE

class Config(object):
    def __init__(self, json):
        self._json = json
        
    @classmethod
    def get(cls):
        try:
            with open(CONFIGFILE, 'r') as f:
                return cls(json.loads(f.read()))
        except FileNotFoundError as e:
            logging.warning("creating new config file")
            return cls(TEMPLATE)

    def __getitem__(self, key):
        return self._json[key]

    def __delitem__(self, key):
        del self._json[key]

    def __setitem__(self, key, value):
        self._json[key] = value

    def save(self):
        with open(CONFIGFILE, 'w') as f:
            f.write(json.dumps(
                self._json,
                indent=4, separators=(',', ': ')))


config = Config.get()
