#! /bin/sh

docker run -it -v ~/mnt:/mnt -v /srv/csv:/srv/csv -v /cevac/cache:/cevac/cache live:test "$@"
