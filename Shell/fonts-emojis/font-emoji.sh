#!/bin/bash

os=`lsb_release -d | awk -F"\t" '{print $2}'`

if echo ${os} | grep -i 'ubuntu\|debian'; then
    sudo apt-get install fonts-noto-color-emoji
else
    sudo dnf install google-noto-emoji-color-fonts
fi

config_location="~/.config/fontconfig/"

mkdir -p $config_location

mv fonts.conf $config_location

fc-cache -f
