#!/bin/bash

#First arg is team member name
#Second arg is Hiren's drive letter. Defaults to b if no argument.

#Exits with message if there are no arguments
if [ -z $1 ]; then
    echo "Enter an argument"
    exit 1
fi

#Defaults drive letter to b. Assigns arg2 if it exists.
drive="/dev/sd${2}1"
if [ -z $2 ]; then
    drive="/dev/sdb1"
fi

mount $drive /mnt
rm -r /tmp/BurnInTest
mkdir /tmp/BurnInTest

if [ $1 = dj ]; then
    cp ./wav/swagga.wav /tmp/BurnInTest/Testsound.wav
fi

if [ $1 = tyler ]; then
    cp ./wav/default.wav /tmp/BurnInTest/Testsound.wav
fi

if [ $1 = jordan ]; then
    cp ./wav/chair.wav /tmp/BurnInTest/Testsound.wav
fi

if [ $1 = john ]; then
    cp ./wav/countryboy.wav /tmp/BurnInTest/Testsound.wav
fi

if [ $1 = sarah ]; then
    cp ./wav/firepower.wav /tmp/BurnInTest/Testsound.wav
fi

if [ $1 = repair ]; then
    cp ./wav/sax.wav /tmp/BurnInTest/Testsound.wav
fi

if [ $1 = jesse ]; then
    cp ./wav/default.wav /tmp/BurnInTest/Testsound.wav
fi

if [ $1 = james ]; then
    cp ./wav/default.wav /tmp/BurnInTest/Testsound.wav
fi

if [ $1 = default ]; then
    cp ./wav/default.wav /tmp/BurnInTest/Testsound.wav
fi

7z a /mnt/HBCD/Programs/Files/BurnInTest.7z /tmp/BurnInTest
umount /mnt
