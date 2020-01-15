#! /bin/sh

docker build . -t live:test
rm -rf src/*
cp -r ~/mnt/* src/
