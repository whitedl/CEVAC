#! /bin/sh

docker save -o /cevac/docker_images/live_test.tar live:test
rsync live_test.tar bmeares@fmo14:~/docker/live_test.tar
ssh bmeares@fmo14 "docker load -i ~/docker/live_test.tar"
