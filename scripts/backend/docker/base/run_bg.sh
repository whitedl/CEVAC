#! /bin/sh
. /cevac/docker/config.sh

docker run -d -v ~/mnt/CEVAC_python:/mnt -v /srv/csv:/srv/csv -v /cevac:/cevac -v ~/.ssh/:/root/.ssh "$image" "$@"

