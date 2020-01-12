FROM ubuntu:18.04
# FROM python:3
MAINTAINER Bennett Meares <bmeares@g.clemson.edu>
RUN apt-get update && apt-get install python3 python3-pip unixodbc unixodbc-dev curl openssh-server -y
RUN pip3 install pandas sqlalchemy pyodbc cx_Oracle
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.10/prod.list > /etc/apt/sources.list.d/mssql-release.list && apt-get update
RUN ACCEPT_EULA=Y apt-get install msodbcsql17 -y
ADD . /root/
RUN pip3 install /root/src/Facilities_python
WORKDIR /root/src/CEVAC_python/CEVAC/
# WORKDIR /mnt/src/CEVAC_python/CEVAC/
# ENTRYPOINT ["/bin/bash"]
CMD ["python3","main.py","-x","live"]
