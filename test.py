#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

        print res

    except Exception, e:
        print e


if __name__ == "__main__":
    execute_monitor()