#!/bin/bash

os=`lsb_release -d | awk -F"\t" '{print $2}'`
config_location="~/.config/fontconfig/"

mkdir -p $config_location


if echo ${os} | grep -i 'ubuntu\|debian'; then
    sudo apt-get install -y fonts-noto-color-emoji
    mv fonts-ubuntu.conf ${config_location}/fonts.conf
else
    sudo dnf install -y google-noto-emoji-color-fonts
    mv fonts-fedora.conf ${config_location}/fonts.conf
fi


fc-cache -f
