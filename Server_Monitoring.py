import os
import sys
import psutil as ps
from tabulate import tabulate
import numpy as np


process_data = [[ "PID", "Process Name", "CPU Usage", "Memory Usage"]]


def cpu_monitoring():
    print "Total CPU Consuming: " + str(ps.cpu_percent(1, False)) + "%"
    print "CPU Consuming Per Core: " + str(ps.cpu_percent(1, True))

    #Should add writing to a csv file.


def memory_usage_mon():
    print "Total Memory In The Server: " + str(round(float(ps.virtual_memory()[0]) / 1000000000, 2)) + " GB "
    print "Available Memory In The Server: " + str(round(float(ps.virtual_memory()[1]) / 1000000000, 2)) + " GB "
    print "Memory Usage: " + str(round(float(ps.virtual_memory()[2]), 2)) + " % "
    print "Used Memory: " + str(round(float(ps.virtual_memory()[3]) / 1000000000, 2)) + " GB "
    print "Free Memory: " + str(round(float(ps.virtual_memory()[4]) / 1000000000, 2)) + " GB "


def processes_monitoring(process_data):
    for item in ps.pids():
        p = ps.Process(item)
        new_line = [[str(p.pid), str(p.name()),  str(p.cpu_percent(interval=0.01)), str(round(p.memory_percent() / 1000000, 2))]]
        process_data = np.append(process_data, new_line, axis=0)
    return process_data


print "CPU"
print "============"
cpu_monitoring()
print "\n"
print "Memory"
print "============"
memory_usage_mon()
print "\n"
print "Task list"
print "============"
process_data = processes_monitoring(process_data)
print tabulate(process_data, headers="firstrow", showindex="always")
