#!/usr/bin/env python3
import subprocess
import re
# Remove APT cache
def removeaptcache(self):
    print("APTcache size is {}. Are you remove it? Y/n")

def get_aptcachesize(self):
    return subprocess.check_output(["echo", "${$(du", "-s", "/var/cache/apt)%%/var/cache/apt}"])

def removeit(self):
    return subprocess.check_output(["apt-get", "clean"])


# Remove old kernels
def removekernel():
    def get_oldkernels():
        version = subprocess.run(r'dpkg -l | grep -Eo "linux-image-[0-9]+\.[0-9]+\.[0-9]+-[0-9]" | grep -Eo "[0-9]+\.[0-9]+\.[0-9]+-[0-9]+" | uniq | sort -nr', shell=True, stdout=subprocess.PIPE)
        installing = version.splitlines()
        del installing[0]
        olders = tuple(installing)
        return olders

    def formating(*args):# args type = string ! Do not number
        olders = []
        for i in range(len(args)):
            olders.append(args[i][i])
        
        terget = ("linux-headers-", "linux-image-")
        removed = []
        for version in olders:
            for tgt in terget:
                removed.append(tgt + version)
        #removed = [tgt + version for version in olders for tgt in terget ]
        return removed

    def removethem(*args):
        removed = []
        for i in range(len(args)):
            for n in range(len(args[i])):
                removed.append(args[i][n])
        return subprocess.call(["apt-get", "autoremove", "--purge", "-y", removed])

    #Main
    print("These kernels removed. {}".format(get_oldkernels()))
    print("Are you remove them? Y/n")
    anser = yesno(input())
    if anser == True:
        removethem(formating(get_oldkernels()))
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

removekernel()
