import os
import sys
import psutil as ps
from tabulate import tabulate   #In order to print tables
import subprocess               #In order to use SSH connection
from shutil import copyfile     #In order to copy files
import numpy as np
import plotly
from time import gmtime, strftime


#TO ADD ARGUMENTS INSERTION AND OUTPUT SELECTION


def ssh_connection():
    HOST="www.example.org"
    # Ports are handled in ~/.ssh/config since we use OpenSSH
    COMMAND="uname -a"

    ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
        print >>sys.stderr, "ERROR: %s" % error
    else:
        print result



def cpu_monitoring():
    return "Total CPU Consuming: " + str(ps.cpu_percent(1, False)) + "%\n" + "CPU Consuming Per Core: " + str(ps.cpu_percent(1, True))


    #Should add writing to a csv file.



def memory_usage_mon():
    return ("Total Memory In The Server: " + str(round(float(ps.virtual_memory()[0]) / 1000000000, 2)) + " GB \n"
    + "Available Memory In The Server: " + str(round(float(ps.virtual_memory()[1]) / 1000000000, 2)) + " GB \n"
    + "Memory Usage: " + str(round(float(ps.virtual_memory()[2]), 2)) + " % \n"
    + "Used Memory: " + str(round(float(ps.virtual_memory()[3]) / 1000000000, 2)) + " GB \n"
    + "Free Memory: " + str(round(float(ps.virtual_memory()[4]) / 1000000000, 2)) + " GB \n\n\n")



def processes_monitoring(data):
    for item in ps.pids():
        p = ps.Process(item)
        new_line = [[str(p.pid), str(p.name()),  str(p.cpu_percent(interval=0.01)), str(round(p.memory_percent() / 1000000, 2))]]
        data = np.append(data, new_line, axis=0)
    return data


def log_files_copy():
    copyfile(src, dst)
    print "I did a copy"


def pinger():
    print "my ping"


def configuration_file_extraction():
    copyfile("\usr\share\apache-tomcat8\webapps\logs", dst)


def create_summary():
    file_name = "Machine_Summary"+"_"+str(strftime("%d%m%Y_%H%M%S", gmtime()))+".txt"

    f = open(file_name, 'w')


    f.write("CPU Usage\n==========\n" + cpu_monitoring()+'\n\n\n')
    print "CPU Usage was written to file\n"


    f.write("Memory Usage\n==========\n" + memory_usage_mon())
    print "Memory Usage was written to file \n"


    process_data = [["PID", "Process Name", "CPU Usage", "Memory Usage"]]
    process_data = processes_monitoring(process_data)
    f.write("Running Processes\n=================\n" + tabulate(process_data, headers="firstrow", showindex="always"))
    print "Task List was written to file\n"


create_summary()