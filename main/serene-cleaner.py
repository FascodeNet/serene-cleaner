#!/usr/bin/env python3
import subprocess
import os.path
class Cleancache():
    def __init__(self, path):
        rpath = path + r"/*"
        self.searchpath = path.split()
        self.removepath = rpath
        self.checkpath = ""
    def get_cachesize(self):
        cmd = ["du", "-sm",]
        cmd.extend(self.searchpath)
        output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        rawout = output.stdout.decode("UTF-8")
        size = [int(s) for s in rawout.split() if s.isdigit()][0]
        return size
    def check_exists(self):
        return os.path.exists(self.checkpath)

    def cleanit(self):
        cmd = "sudo rm -r " + self.removepath
        subprocess.run(cmd, shell=True)
        return "0"


class Cleanaptcache(Cleancache):
    def __init__(self):
        path = r"/var/cache/apt"
        super().__init__(path)
        self.checkpath = path + r"/package.bin"
    def main(self):
        if self.check_exists() == False:
            print("Do not have to clean APT cache.\n")
            return 0
        print("APT cache size is {} MiB.".format(self.get_cachesize()))
        print("Are you clean it?\nYes/no")
        anser = yesno(input(">"))
        if anser == True:
            self.cleanit()
        else:
            return 0

class Cleanchromiumcache(Cleancache):
    def __init__(self):
        homedir = get_homedir()
        path = homedir + r"/.cache/chromium/Default/Cache"
        super().__init__(path)
        self.checkpath = path + r"/index"
    def main(self):
        if self.check_exists() == False:
            print("Do not have to clean Chromium cache or Chromium is not installed this computer.\n")
            return 0
        print("Chromium cache is {} MiB.".format(self.get_cachesize()))
        print("Are you clean it?\nYes/no")
        anser = yesno(input(">"))
        if anser == True:
            self.cleanit()
        else:
            return 0


class Removekernel():
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
    
    def main(self):
        print("These package will be removed {}".format(self.get_oldkernels()))
        print("Are you remove them?\nYes/no")
        anser = yesno(input(">"))
        if anser == True:
            self.removethem()
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

def get_homedir():
    output = subprocess.run(["whoami"], stdout=subprocess.PIPE)
    rawout = output.stdout.decode("UTF-8")
    homedir = rawout.rstrip()
    return r"/home/" + homedir

def main():
    print("---------------------------")
    print("|Welcome to serene-cleaner|")
    print("---------------------------")
    while True:

        print("Please choose a task")
        print("1. clean APT cache")
        print("2. clean Chromium cache")
        print("3. remove old kernels")
        print("0. exit")
        anser = input(">")
        if anser == "":
            print("Please type integer\n")
            continue
        choice = 0
        try:
            choice = int(anser[0])
        except ValueError:
            print("Please type integer\n")
            continue

        if choice == 1:
            call = Cleanaptcache()
            call.main()
        elif choice == 2:
            call = Cleanchromiumcache()
            call.main()
        elif choice == 3:
            call = Removekernel()
            call.main()
        elif choice == 0:
            exit(0)
        else:
            print("Please choose from the option\n")
            continue

if __name__ == "__main__":
    main()