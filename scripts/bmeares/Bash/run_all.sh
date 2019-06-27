#! /bin/sh
#
# run_all.sh
# Copyright (C) 2019 bmeares <bmeares@wfic-temp1>
#
# Distributed under terms of the MIT license.
#

time /home/bmeares/scripts/update_power_latest_sum.sh WATT
time /home/bmeares/scripts/update_power_latest_sum.sh ASC

time /home/bmeares/scripts/update_co2_latest_avg.sh WATT
# time /home/bmeares/scripts/update_co2_latest_avg.sh ASC

time /home/bmeares/scripts/update_temp_latest_avg.sh WATT
time /home/bmeares/scripts/update_temp_latest_avg.sh ASC
