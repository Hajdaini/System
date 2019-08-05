#!/bin/bash

sudo dnf install google-noto-emoji-color-fonts

config_location="~/.config/fontconfig/"

mkdir -p $config_location

mv fonts.conf $config_location

fc-cache -f
