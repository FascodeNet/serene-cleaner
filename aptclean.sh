#!/bin/bash
if [[ $UID != 0 ]]; then
    echo "You have to run this as root."
    exit 1
fi
cache_size=$(du -sh /var/cache/apt)
cache_size=${cache_size%%/var/cache/apt}
if [[ $cache_size = *M* ]]; then
	cache_size=${cache_size%%M*}
elif [[ $cache_size = *G* ]]; then
    echo "Cleaning..."
	apt clean
    echo "Done!"
    rm 128
	exit 0
else
    echo "You do not have to clear cache."
    rm 128
    exit 0
fi
if [ [$cache_size] > "128" ]; then
   echo "Cleaning..."
   apt clean
   echo "Done!"
   rm 128
fi
