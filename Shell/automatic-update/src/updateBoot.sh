#!/bin/bash

now=$(date +'[%d/%m/%Y %H:%M:%S]')

logpath="/var/log/updateBoot/"

if [ ! -d $logpath ]; then
  mkdir $logpath;
fi

logfile="$logpath/update.log"
errorfile="$logpath/update_errors.log"

echo -e "\n--------------------------------------" >> $logfile
echo -e "\n--------------------------------------" >> $errorfile
echo -e "$now\n" >> $logfile
echo -e "$now\n" >> $errorfile
dnf upgrade -y 2>> $errorfile 1>> $logfile
