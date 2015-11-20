#!/bin/bash

#Defaults drive letter to b. Assigns arg1 if it exists.
drive="/dev/sd${1}1"
if [ -z $1 ]; then
    drive="/dev/sdb1"
fi

mount $drive /mnt
mkdir /mnt/slax/rootcopy/root
cp /home/testing/linux-testing-scripts/audio.sh /mnt/slax/rootcopy/root/audio.sh
cp /home/testing/linux-testing-scripts/shutdown.sh /mnt/slax/rootcopy/root/shutdown.sh
cp /home/testing/linux-testing-scripts/sound.mp3 /mnt/slax/rootcopy/root/sound.mp3
umount /mnt
