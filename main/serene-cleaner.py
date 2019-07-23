#!/usr/bin/env python3
import subprocess
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
        output = subprocess.run(r'dpkg -l | grep -Eo "linux-image-[0-9]+\.[0-9]+\.[0-9]+-[0-9]+[0-9]" | grep -Eo "[0-9]+\.[0-9]+\.[0-9]+-[0-9]+" | uniq | sort -nr', shell=True, stdout=subprocess.PIPE)
        version = output.stdout.decode("UTF-8")
        installing = version.splitlines()
        del installing[0]
        if not installing:
            print("Do not have to remove old kernel.")
            exit(0)
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
        removed_l = []
        for i in range(len(args)):
            for n in range(len(args[i])):
                removed_l.append(args[i][n])
        cmd = "sudo apt-get --purge -y autoremove"
        command_l = cmd.split()
        command_l.extend(removed_l)
        subprocess.call(command_l)

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
