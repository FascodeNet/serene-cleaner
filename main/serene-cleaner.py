#!/usr/bin/env python3
import subprocess
import argparse
import re

task_dict = {"clean APT cache": "cleanaptcache", "remove old kernels": "removekernel"}

# Remove APT cache
def cleanaptcache():
    print("APT-cache size is {}MiB.\nAre you clean it?".format(get_aptcachesize()))
    anser = yesno(input("Y/n "))
    if anser == True:
        cleanit()
    else:
        return 0

def get_aptcachesize():
    output = subprocess.run(["sudo", "du", "-sm", "/var/cache/apt"], stdout=subprocess.PIPE)
    rawout =  output.stdout.decode("UTF-8")
    size = [int(s) for s in rawout.split() if s.isdigit()][0]
    return size

def cleanit():
    return subprocess.check_output(["sudo", "apt-get", "clean"])


# Remove old kernels
def removekernel():
    olders = []
    removed = []
    def get_oldkernels():
        global olders
        global removed
        output = subprocess.run(r'dpkg -l | grep -Eo "linux-image-[0-9]+\.[0-9]+\.[0-9]+-[0-9]+[0-9]" | grep -Eo "[0-9]+\.[0-9]+\.[0-9]+-[0-9]+" | uniq | sort -nr', shell=True, stdout=subprocess.PIPE)
        rawout = output.stdout.decode("UTF-8")
        installing = rawout.splitlines()
        del installing[0]
        olders = installing
        if not installing:
            print("Do not have to remove old kernel.")
            exit(0)
        terget = ("linux-headers-", "linux-image-")
        removed = [tgt + version for version in olders for tgt in terget ]
        return removed

    def removethem():
        global removed
        cmd = "sudo apt-get --purge -y autoremove"
        command_l = cmd.split()
        command_l.extend(removed)
        subprocess.call(command_l)

    #Main
    print("These kernels removed. {}".format(get_oldkernels()))
    print("Are you remove them? Y/n")
    anser = yesno(input())
    if anser == True:
        removethem()
    else:
        return 0


#Others
def yesno(choice):
    if choice == "":
        return True
    
    choice = choice[0]
    while True:
        if choice.upper() == 'Y':
            return True
        elif choice.upper() == 'N':
            return False
        else:
            return "Error"

def swich(choice):
    if choice == "":
        return "Error"
    try:
        choice = int(choice[0])
    except ValueError:
        return "Please enter as an integer."
    try:
        task = list[choice - 1]
    except IndexError:
        return "The task is not find."
    return task