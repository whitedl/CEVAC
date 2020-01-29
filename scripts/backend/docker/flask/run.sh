#! /bin/sh
. /cevac/docker/config.sh

docker run -it -v ~/docker/flask/src:/mnt -v /srv/csv:/srv/csv -v /cevac:/cevac -v ~/.ssh/:/root/.ssh "$image" "$@"

