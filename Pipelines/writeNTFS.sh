#!/bin/zsh

DRIVER_NAME=$1
uuid=`diskutil info /Volumes/$DRIVER_NAME | grep UUID | sed -E 's/Volume UUID:[[:space:]]+(.+)/\1/'`
sudo echo "UUID=$uuid none ntfs rw,auto,nobrowse" >> /etc/fstab
