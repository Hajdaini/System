#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run the script from the root user"
  exit
fi


crontab -l -u root | cat - src/crontab | crontab -

location="/usr/local/bin/updateBoot/"

mkdir -p $location

cp src/updateBoot.sh $location
cp src/updateBootLog.sh $location
cp src/updateBoot.service /etc/systemd/system

chmod +x $location/updateBoot.sh
chmod +x $location/updateBootLog.sh


systemctl start updateBoot
systemctl enable updateBoot
