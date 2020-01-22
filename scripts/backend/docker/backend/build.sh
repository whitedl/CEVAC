#! /bin/sh
. ./config.sh
rm -rf src/*
cp -r ~/mnt/* src/
docker build . -t "$image"
rm -rf src/*
