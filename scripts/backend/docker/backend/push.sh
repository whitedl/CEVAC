#! /bin/sh

. ./config.sh

docker save -o /cevac/docker_images/"$filename" "$image"
rsync /cevac/docker_images/"$filename" bmeares@fmo14:~/docker/"$filename"
ssh bmeares@fmo14 "docker load -i ~/docker/$filename"

