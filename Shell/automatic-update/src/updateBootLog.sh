#!/bin/bash

logfile="/var/log/updateBoot/update.log"

if [ -f $logfile  ] ; then
	mv $logfile /var/log/updateBoot/$(date +'update_%d_%m_%Y_%M.log')
else
	touch $logfile
fi