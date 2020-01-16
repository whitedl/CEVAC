#! /bin/sh

rm -rf src/*
cp -r ~/mnt/* src/
docker build . -t live:test
