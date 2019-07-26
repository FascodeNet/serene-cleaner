#!/usr/bin/env python3
import subprocess

class clearcache():
    def __init__(self, path):
        rpath = path + r"/*"
        self.searchpath = path.split()
        self.removepath = rpath
    def get_cachesize(self):
        cmd = ["du", "-sm",]
        cmd.extend(self.searchpath)
        output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        rawout = output.stdout.decode("UTF-8")
        size = [int(s) for s in rawout.split() if s.isdigit()][0]
        return size
    def cleanit(self):
        cmd = "sudo rm -r " + self.removepath
        subprocess.run(cmd, shell=True)
        return "Done"

# Remove old kernels
class removekernel():
    removed = []
    @classmethod
    def get_oldkernels(self):
        output = subprocess.run(r'dpkg -l | grep -Eo "linux-image-[0-9]+\.[0-9]+\.[0-9]+-[0-9]+[0-9]" | grep -Eo "[0-9]+\.[0-9]+\.[0-9]+-[0-9]+" | uniq | sort -nr', shell=True, stdout=subprocess.PIPE)
        rawout = output.stdout.decode("UTF-8")
        installing = rawout.splitlines()
        del installing[0]
        olders = installing
        if not installing:
            print("Do not have to remove old kernel.")
            exit(0)
        terget = ("linux-headers-", "linux-image-")
        self.removed = [tgt + version for version in olders for tgt in terget ]
        return self.removed
    @classmethod
    def removethem(self):
        cmd = "sudo apt-get --purge -y autoremove"
        command_l = cmd.split()
        command_l.extend(self.removed)
        subprocess.call(command_l)



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

inst = clearcache(r"/var/cache/apt")
#Main
print("APT-cache size is {}MiB.\nAre you clean it?".format(inst.get_cachesize()))
anser = yesno(input("Y/n "))
if anser == True:
    inst.cleanit()
else:
    exit(0)
