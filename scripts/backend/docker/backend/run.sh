#! /bin/sh
. /cevac/docker/config.sh

docker run -it -v ~/mnt/CEVAC_python:/mnt -v /srv/csv:/srv/csv -v /cevac:/cevac -v ~/.ssh/:/root/.ssh "$image" "$@"

