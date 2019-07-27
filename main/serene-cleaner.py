#!/usr/bin/env python3
import subprocess
import os.path
import tkinter as tk

root = tk.Tk()
root.title("serene-cleaner")
root.geometry("640x480")
root.mainloop()

class cleancache():
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

    def check_dir(self, file):
        return os.path.isfile(self.path + r"/" + file)

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
            #Do not have to remove old kernel.
            return 0
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