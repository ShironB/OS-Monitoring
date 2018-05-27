"""
Flow
======
    1. Starting the program is done by shell command (--linux or --win).
    2. Appropriate menu (Linux or Windows) will pop up.
    3. Currently supporting Linux only ( 3 Options: 1. SSH connection to relevant servers
                                                    2. Execute Server Summary report
                                                    3. Pinger - Not Yet Finished)


Tasks
======
    1. Writing main GUI for windows - with selection for the function to run.
    2. Pinger function for Linux - need to complete writing to logs.
    3. SSH connection - need to write module to open ssh within Windows OS.
    4. Import Libraries based on OS.


Tests
======
    1. Test SSH connection in LINUX.
    2. Test the initial outputs which depeneds on the arguments.

"""

import os
import sys
import psutil as ps
from tabulate import tabulate       # In order to print tables
from shutil import copyfile         # In order to copy files
import numpy as np
from time import gmtime, strftime
if 'darwin' in sys.platform:
    my_os = 'osx'
    import pexpect
elif 'linux' in sys.platform:
    my_os = 'linux'
    import pexpect
    import subprocess               # In order to use SSH connection
elif 'win32' in sys.platform:
    import winpexpect
    import Tkinter as tk            # In order to use GUI options
    from Tkinter import *
    import ttk
else:
    my_os = 'unknown:' + sys.platform
    import pexpect


# Linux
# -----------
# SSH Connection To Production Servers - Linux OS
def sshconnectionmanu():
    def sshconnectionmanagerlinux(host):
        COMMAND = "uname -a"

        ssh = subprocess.Popen(["ssh", "%s" % host, COMMAND],
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        if result == []:
            error = ssh.stderr.readlines()
            print >> sys.stderr, "ERROR: %s" % error
        else:
            print result

    print "#######################################"
    print "                                       "
    print "           Servers List:               "
    print "1. LIVE - APP                          "
    print "2. LIVE - Mongo                        "
    print "3. Beurer - APP                        "
    print "4. Beurer - Mongo                      "
    print "5. Verlo - APP                         "
    print "6. Verlo - Mongo                       "
    print "7. iFIT - APP                          "
    print "8. iFIT - Mongo                        "
    print "9. lilac                               "
    print "                                       "
    print "#######################################"

    serversnames = ['prod-app-live1', 'prod-mongo-live1', 'prod-app-brr1', 'prod-mongo-brr1', 'prod-app-verlo1',
                    'prod-mongo-verlo1', 'prod-app-icn1', 'prod-mongo-icn1', 'lilac']
    userresponsessh = raw_input("Please enter your selection: ")

    if 'win32' in sys.platform:
        print 'no can do'
    else:
        sshconnectionmanagerlinux(serversnames[int(userresponsessh) - 1])


# System Performance Summary Creation - Linux OS
def create_summary():
    def cpu_monitoring():
        return "Total CPU Consuming: " + str(ps.cpu_percent(1, False)) + "%\n" + "CPU Consuming Per Core: " + str(
            ps.cpu_percent(1, True))


        # Should add writing to a csv file.

    def memory_usage_mon():
        return ("Total Memory In The Server: " + str(round(float(ps.virtual_memory()[0]) / 1000000000, 2)) + " GB \n"
                + "Available Memory In The Server: " + str(
            round(float(ps.virtual_memory()[1]) / 1000000000, 2)) + " GB \n"
                + "Memory Usage: " + str(round(float(ps.virtual_memory()[2]), 2)) + " % \n"
                + "Used Memory: " + str(round(float(ps.virtual_memory()[3]) / 1000000000, 2)) + " GB \n"
                + "Free Memory: " + str(round(float(ps.virtual_memory()[4]) / 1000000000, 2)) + " GB \n\n\n")

    def processes_monitoring(data):
        for item in ps.pids():
            p = ps.Process(item)
            new_line = [[str(p.pid), str(p.name()), str(p.cpu_percent(interval=0.01)),
                         str(round(p.memory_percent() / 1000000, 2))]]
            data = np.append(data, new_line, axis=0)
        return data

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


# Pinger for linux - Not Yet Finished
def machines_pinger_lin():
    machines_lst = []
    file_names = []
    f = []
    amount = int(input("Please enter amount of machines to ping:\n"))

    for i in range(0, amount):
        machines_lst.append(raw_input("\nPlease enter IP for the %d machine:\n" % (i+1)))
        file_names.append("Pinger_Report_" + machines_lst[i] + "_" + str(strftime("%d%m%Y_%H%M%S", gmtime())) + ".txt")

    for i in range(0, amount):
        print i
        f = open(file_names[i], 'w')
        print str(os.system("Ping " + machines_lst[0] + ">" + file_names[i]))
        # ping_output = str(os.system("Ping " + machines_lst[0] + ">" + file_name))

        f.write(str(strftime("%d%m%Y_%H%M%S", gmtime())) + " - ")
        f.close

        ''' f = open(file_name, 'r')
        lines = f.readlines()
        f.seek(0)
        f.close

        f = open(file_name, 'w')
        for item in lines:
            if 'Reply' in item:
                f.write(item)
'''


# Exctract The Properties File Out Of The Folder - Not Yet Finished
def properties_file_extraction():
    copyfile("\usr\share\\apache-tomcat8\webapps\logs", dst)


# Function Which Help To Copy Log Files To tmp Folder In Ansible. - Not Yet Finished
def log_files_copy():
    copyfile(src, dst)
    print "I did a copy"


# Windows GUI
# ---------------------
# Quiting Windows GUI
def quit():
    global root
    root.destroy()


# Gui For Pinger.
def machines_pinger_win():
    global machineamount_w, tkOpenList

    def openentries():
        global e

        tkOpenList.configure(state='disabled')
        amount = int(machineamount_w.get())
        e = ['']

        for i in range(0, amount):
            tklabeleventid = ttk.Label(root, text='  Enter the %d machine IP : ' % int(i + 1))
            tklabeleventid.grid(row=i + 3, column=0)

            e[i] = Entry(root, relief=RIDGE)
            e[i].grid(row=i + 3, column=1, sticky=NSEW)
            e.append('')

        e.remove('')
        tkbuttonstart = tk.Button(root, text="Start", command=pingstart)
        tkbuttonstart.grid(row=i + 4, column=1)

    def pingstart():
        amount = int(machineamount_w.get())

        for i in range(0, amount):
            file_name = "Pinger_Report_" + str(e[i].get()) + "_" + str(strftime("%d%m%Y-%H%M%S", gmtime())) + ".txt"

        ping_output = os.popen("Ping " + str(e[0].get())).read()

        f2 = open('temp.txt', 'w')
        f2.write(ping_output)
        f2.close

        f2 = open('temp.txt', 'r')
        lines = f2.readlines()
        f2.seek(0)

        f = open("Logs/" + file_name, 'w')
        for item in lines:
            if 'Reply' in item:
                f.write(str(strftime("%d.%m.%Y %H:%M:%S", gmtime())) + ' - ' + item)

        f2.close
        # os.remove("temp.txt")


    machineamount_w = tk.StringVar()

    # Amount Label
    tklabeleventid = ttk.Label(root, text='  Amount of machines to ping ')
    tklabeleventid.grid(row=1, column=0)

    # Amount Entry Field
    amountfield = ttk.Entry(root, width=15, textvariable=machineamount_w)
    amountfield.focus()
    amountfield.grid(row=1, column=1)

    tkOpenList = tk.Button(root, text="Enter", command=lambda: openentries())
    tkOpenList.grid(row=2, column=2)

    '''IF MORE THEN 10 Display Pop UP'''

    # Dummy Label
    for i in range(2, 15):
        tklabeleventid2 = ttk.Label(root, text='  ')
        tklabeleventid2.grid(row=i, column=3)


    tkButtonQuit = tk.Button(root, text="Quit", command=quit)
    tkButtonQuit.grid(row=16, column=3)



# Main
# ---------------------
if len(sys.argv) < 1:
    print ("\n")
    print ("Usage: ServerM.py < Argument >")
    print ("Use -h or --help argument to get arguments options ")
    print ("\n")
else:
    if (sys.argv[1]) == "--help":
        print ("\n")
        print ("-win or --win: run the Windows version")
        print ("-linux or --linux: run the Windows version")
        print ("\n")
    if (sys.argv[1]) == "-h":
        print ("\n")
        print ("-win or --win: run the Windows version")
        print ("-linux or --linux: run the Windows version")
        print ("\n")
    if (sys.argv[1]) == "--win" or (sys.argv[1]) == "-win":
        root = tk.Tk()
        root.title("EarlySense Pinger")
        root.geometry("460x394")
        root.resizable(0, 0)

        icon = PhotoImage(file='images\icon.gif')
        root.tk.call('wm', 'iconphoto', root._w, icon)

        machines_pinger_win()

        root.mainloop()
    elif (sys.argv[1]) == "--linux" or (sys.argv[1]) == "-linux":
        userresponse = '0'
        while userresponse == '0':
            print "#######################################"
            print "                                       "
            print "                 Menu:                 "
            print "1. SSH Connection                      "
            print "2. Create Server Performance Summary   "
            print "3. Pinger                              "
            print "                                       "
            print "                                       "
            print "#######################################"

            print sys.platform
            userresponse = raw_input("Please enter your selection: ")
            if userresponse == '1':
                sshconnectionmanu()
            elif userresponse == '2':
                create_summary()
            elif userresponse == '3':
                machines_pinger_lin()
            else:
                print "Command not allowed"