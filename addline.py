#!/usr/bin/env python3

import argparse
import configparser
import logging
import pprint

import bvg
from config import config

parser = argparse.ArgumentParser()
parser.add_argument("lines", type=str, nargs="+", help="BVG line name")
args = parser.parse_args()

l = logging.getLogger(__name__)

def main():
    l.info("Using config: {}".format(bvg.CONFIGFILE))
    config['lines'].extend(args.lines)
    l.info(f'Added {args.lines} to config')
    config.save()

if __name__ == "__main__":
    main()
