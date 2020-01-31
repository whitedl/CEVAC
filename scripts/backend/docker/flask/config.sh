#! /bin/sh

image="cevac:admin"
filename=$(echo "$image" | sed -e "s/:/_/g")".tar"
port="5000"
mnt="/home/cevac/docker/flask/src"
