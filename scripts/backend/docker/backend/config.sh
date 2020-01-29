#! /bin/sh

image="cevac:base"
filename=$(echo "$image" | sed -e "s/:/_/g")".tar"
