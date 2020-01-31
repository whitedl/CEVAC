FROM ubuntu:18.04
MAINTAINER Bennett Meares <bmeares@g.clemson.edu>
ADD ./setup.sh /setup/
RUN /setup/setup.sh
ADD ./src /root/
RUN pip install /root/CEVAC_python
WORKDIR /root/CEVAC_python/
