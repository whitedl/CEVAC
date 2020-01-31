#! /bin/sh
. ./config.sh
docker run -it -v "$mnt":/mnt -v /srv/csv:/srv/csv -v /cevac:/cevac -v ~/.ssh/:/root/.ssh -p "$port":"$port" "$image" "$@"

