#! /bin/sh
. ./config.sh

docker run -it -v ~/mnt:/mnt -v /srv/csv:/srv/csv -v /cevac/cache:/cevac/cache -v ~/.ssh/:/root/.ssh "$image" "$@"

