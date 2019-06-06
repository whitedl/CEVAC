#! /bin/sh
#
# seperator.sh
# Copyright (C) 2019 bmeares <bmeares@wfic-temp1>
#
# Distributed under terms of the MIT license.
#


GREEN_BG="\033[102m"
RESET="\e[0m"
BLOCK="$GREEN_BG $RESET"
width=$(tput cols)
seperator=''
for i in `seq 1 $width`; do
  seperator="$seperator$BLOCK"
done
printf "$seperator\n\n"


