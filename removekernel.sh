#!/bin/bash
if [[ $UID != 0 ]]; then
  echo "You have to run this as root."
  exit 1
fi
LATEST=$(dpkg --list | grep -E -o "linux-image-[0-9]+\.[0-9]+\.[0-9]+-[0-9]+-generic" | grep -o -E "[0-9]+\.[0-9]+\.[0-9]+-[0-9]+" | uniq | sort -n -r | head -1)
TARGETS=$(dpkg --list | grep -E -o "linux-image-[0-9]+\.[0-9]+\.[0-9]+-[0-9]+-generic" | grep -o -E "[0-9]+\.[0-9]+\.[0-9]+-[0-9]+" | uniq | grep -E -v ${LATEST})
echo "These kernel will be removed."
echo $TARGETS
echo "Are you removed these? Y/N"
read yes_or_no
case $yes_or_no in
    "" | [Yy]* )

        ;;
    * )
        exit 0
        ;;
esac
for pkg_ver in ${TARGETS}
do
  for pkg_prefix in linux-headers- linux-image-
  do
    apt-get autoremove --purge -y ${pkg_prefix}${pkg_ver}*
  done
done
update-grub
