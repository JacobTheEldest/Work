#!/bin/bash

#Defaults drive letter to b. Assigns arg1 if it exists.
drive="/dev/sd${2}1"
if [ -z $2 ]; then
    drive="/dev/sdb1"
fi

#mount usb and prepare folders
mount $drive /mnt
if [ ! -d /mnt/slax/rootcopy/root ]; then
    mkdir /mnt/slax/rootcopy/root
fi

#Copy appropriate files according to arguments

if [ $1 = help ]; then
    echo "audio"
    echo "slaxwipe"

fi

if [ $1 = audio ]; then
    cp ../linux-testing-scripts/audio.sh /mnt/slax/rootcopy/root/audio.sh
    cp ../linux-testing-scripts/shutdown.sh /mnt/slax/rootcopy/root/shutdown.sh
    cp ../linux-testing-scripts/sound.mp3 /mnt/slax/rootcopy/root/sound.mp3
fi

if [ $1 = slaxwipe ]; then
    cp ../linux-testing-scripts/slaxwipe.sh /mnt/slax/rootcopy/root/slaxwipe.sh
fi

#Close up
umount /mnt
