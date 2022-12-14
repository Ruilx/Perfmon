#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Prefmon agent

"""

__author__ = "Ruilx"
__organization__ = "GT-Soft"

import argparse
import sys

from config import Config


def argBuilder():
    argparser = argparse.ArgumentParser(sys.argv[0], description="Prefmon agent")
    argparser.add_argument("-c", "--config", type=str, required=True, help="config file", dest="config")
    return argparser.parse_args()


def main():
    args = argBuilder()
    cfg = Config(args.config)
    print(cfg.getAgentName())


if __name__ == '__main__':
    main()
