#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import time
from common.daemon import Daemon
from common.logger import Logger


def main():
    while True:
        Logger.logger.info("daemon function execute")
        time.sleep(1)


class MyDaemon(Daemon):
    def __init__(self, pid):
        super(self.__class__, self).__init__(pid)

    def run(self):
        main()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', default="start", help='start, stop, restart')
    parser.add_argument('-p', '--pidfile', default="./proc/pycommon.pid")

    args = parser.parse_args()
    pidpath = os.path.abspath(args.pidfile)
    dirname = os.path.dirname(pidpath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    daemon = MyDaemon(pidpath)
    if 'start' == args.cmd:
        daemon.start()
    elif 'stop' == args.cmd:
        daemon.stop()
    elif 'restart' == args.cmd:
        daemon.restart()
    else:
        print "Unknown command"
        sys.exit(2)
