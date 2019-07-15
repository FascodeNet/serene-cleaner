#!/bin/bash
LATEST=$(dpkg --list | grep -E -o "linux-image-[0-9]+\.[0-9]+\.[0-9]+-[0-9]+-generic" | grep -o -E "[0-9]+\.[0-9]+\.[0-9]+-[0-9]+" | uniq | sort -n -r | head -1)
TARGETS=$(dpkg --list | grep -E -o "linux-image-[0-9]+\.[0-9]+\.[0-9]+-[0-9]+-generic" | grep -o -E "[0-9]+\.[0-9]+\.[0-9]+-[0-9]+" | uniq | grep -E -v ${LATEST})
echo $TARGETS