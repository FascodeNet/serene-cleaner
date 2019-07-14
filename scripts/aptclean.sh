#!/bin/bash
if [ $UID != 0 ]; then
    echo "You have to run this as root."
    exit 1
fi
get_cache_size(){
    echo ${$(du -s /var/cache/apt)%%/var/cache/apt}
}
clear_cache(){
   apt-get clean
}