#! /bin/sh

. ./config.sh

docker save -o /cevac/docker/"$filename" "$image"
rsync /cevac/docker/"$filename" bmeares@fmo14:~/docker/"$filename"
ssh bmeares@fmo14 "docker load -i ~/docker/$filename"

