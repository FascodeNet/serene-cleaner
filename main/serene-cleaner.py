#!/usr/bin/env python3
import subprocess
# Remove APT cache
def get_aptcachesize(self):
    return subprocess.run(["echo", "${$(du", "-s", "/var/cache/apt)%%/var/cache/apt}"],stdout = subprocess.PIPE, stderr = subprocess.PIPE)

def removeaptcache(self):
    return subprocess.run(["apt-get", "clean"], stderr = subprocess.PIPE)


# Remove old kernels
def get_oldkernels(self):
    return subprocess.run(['dpkg', '--list', '|', 'grep', '-E', '-o', '"linux-image-[0-9]+\\.[0-9]+\\.[0-9]+-[0-9]+-generic"', '|', 'grep', '-o', '-E', '"[0-9]+\\.[0-9]+\\.[0-9]+-[0-9]+"', '|', 'uniq', '|', 'grep', '-E', '-v', '${dpkg', '--list', '|', 'grep', '-E', '-o', '"linux-image-[0-9]+\\.[0-9]+\\.[0-9]+-[0-9]+-generic"', '|', 'grep', '-o', '-E', '"[0-9]+\\.[0-9]+\\.[0-9]+-[0-9]+"', '|', 'uniq', '|', 'sort', '-n', '-r', '|', 'head', '-1}'],stdout = subprocess.PIPE, stderr = subprocess.PIPE)

def formating(*args):# args type = string ! Do not number
    olders = (i for i in args)
    terget = ("linux-headers-", "linux-image-")
    removed = [version + tgt for tgt in olders for version in terget]
    return removed

def removethem(*args):
    removed = args
    return subprocess.run(["apt-get", "autoremove", "--purge", "-y", removed],stderr = subprocess.PIPE)


# Others
def checkroot(self):
    pass
