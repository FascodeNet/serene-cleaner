#!/bin/bash
if [[ $UID != 0 ]]; then
  echo "You have to run this as root."
  exit 1
fi
get_oldkernels(){
  TARGETS=$(dpkg --list | grep -E -o "linux-image-[0-9]+\.[0-9]+\.[0-9]+-[0-9]+-generic" | grep -o -E "[0-9]+\.[0-9]+\.[0-9]+-[0-9]+" | uniq | grep -E -v ${dpkg --list | grep -E -o "linux-image-[0-9]+\.[0-9]+\.[0-9]+-[0-9]+-generic" | grep -o -E "[0-9]+\.[0-9]+\.[0-9]+-[0-9]+" | uniq | sort -n -r | head -1})
  echo $TARGETS
}

remove_oldkernels(){
  # $1 = $TARGETS
  for pkg_ver in $1
  do
    for pkg_prefix in linux-headers- linux-image-
    do
      apt-get autoremove --purge -y ${pkg_prefix}${pkg_ver}*
    done
  done
  update-grub
}