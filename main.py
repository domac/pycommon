#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import time
from common.daemon import Daemon
from common.logger import Logger
import commands


def execute_monitor():
    try:
        cmd_conn_num = "netstat -n | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'"
        cmd_conn_num_code, cmd_conn_num_output = commands.getstatusoutput(
            cmd_conn_num)

        result_cmd_conn_num = "1) connections global status: \n%s" % cmd_conn_num_output

        cmd_conn_num_25432 = "netstat -n | grep 25432 | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'"
        cmd_conn_num_code, cmd_conn_num_output_25432 = commands.getstatusoutput(
            cmd_conn_num_25432)

        result_cmd_conn_num_25432 = "2) connections postgres status: \n%s" % cmd_conn_num_output_25432

        cmd_processes_num = "ps -ef | grep postgres | grep -v 'grep ' | wc -l"
        cmd_processes_num_code, cmd_processes_num_output = commands.getstatusoutput(
            cmd_processes_num)
        cmd_processes_num_output = cmd_processes_num_output.strip()
        result_cmd_processes_num = "3) postgres processes  status: %s" % cmd_processes_num_output

        res = "%s\n%s\n%s" % (result_cmd_conn_num, result_cmd_conn_num_25432,
                              result_cmd_processes_num)

        Logger.logger.info("\n%s" % res)

    except Exception, e:
        Logger.logger.error(e)


flow_counter = {"8081": 0, "28080": 0, "28180": 0, "443": 0}


def execute_port_flow(secs):
    result = {}
    for port, old_counter in flow_counter.items():
        cmd = "iptables -L -v -n -x | grep 'tcp dpt:%s' | awk '{print $2}' | head -n 1" % port
        code, output = commands.getstatusoutput(cmd)
        if not output:
            output = "0"
        new_counter = int(str(output))
        counter = new_counter - old_counter
        flow_counter[port] = new_counter
        if counter == new_counter:
            continue
        result[port] = 8 * counter / 1024 / secs

    output = "net port flow : "
    for port, res in result.items():
        sub = "<%s:%dKb>\t" % (port, res)
        output += sub

    Logger.logger.info(output)


def main():
    while True:
        execute_port_flow(10)
        time.sleep(10)


class ExampleDaemon(Daemon):
    def __init__(self, pid):
        super(self.__class__, self).__init__(pid)

    def run(self):
        if not os.path.exists("/data/logs"):
            os.makedirs("/data/logs")

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
    daemon = ExampleDaemon(pidpath)
    if 'start' == args.cmd:
        daemon.start()
    elif 'stop' == args.cmd:
        daemon.stop()
    elif 'restart' == args.cmd:
        daemon.restart()
    else:
        print "Unknown command"
        sys.exit(2)
