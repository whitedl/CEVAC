#! /bin/sh

image="cevac:backend"
filename=$(echo "$image" | sed -e "s/:/_/g")".tar"
