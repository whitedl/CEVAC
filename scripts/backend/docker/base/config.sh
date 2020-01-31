#! /bin/sh

image="cevac:base"
mnt="/home/cevac/docker/base/src"
filename=$(echo "$image" | sed -e "s/:/_/g")".tar"
