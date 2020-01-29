#! /bin/sh

image="cevac:admin"
filename=$(echo "$image" | sed -e "s/:/_/g")".tar"
