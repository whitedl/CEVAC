#! /bin/sh

out=`if ! echo "test" ; then exit 1`
echo "$out"
