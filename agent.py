#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Prefmon agent

"""

import argparse
import sys
from cfg import Cfg


def argBuilder():
    argparser = argparse.ArgumentParser(sys.argv[0], description="Prefmon agent")
    argparser.add_argument("-c", "--config", type=str, required=True, help="config file", dest="config")
    return argparser.parse_args()


def main():
    args = argBuilder()
    cfg = Cfg(args.config)
    print(cfg.getAgentName())


if __name__ == '__main__':
    main()