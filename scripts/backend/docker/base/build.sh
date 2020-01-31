#! /bin/sh
. ./config.sh
docker build . -t "$image"
