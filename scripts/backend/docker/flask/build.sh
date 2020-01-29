#! /bin/sh
. ./config.sh
rm -rf src/*
cp -r ~/mnt/* src/
docker build --no-cache . -t "$image"
rm -rf src/*
