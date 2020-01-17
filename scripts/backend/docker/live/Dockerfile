FROM ubuntu:18.04
# FROM python:3
MAINTAINER Bennett Meares <bmeares@g.clemson.edu>
RUN apt-get update && apt-get install python3.7 python3-pip python3.7-dev unixodbc unixodbc-dev curl openssh-server -y
RUN python3.7 -m pip install pip --upgrade
RUN pip install pandas sqlalchemy pyodbc cx_Oracle pyyaml paramiko
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.10/prod.list > /etc/apt/sources.list.d/mssql-release.list && apt-get update
RUN ACCEPT_EULA=Y apt-get install msodbcsql17 -y
ADD . /root/
RUN pip install /root/src/Facilities_python
RUN pip install /root/src/CEVAC_python
WORKDIR /root/src/CEVAC_python/
# WORKDIR /mnt/src/CEVAC_python/CEVAC/
# ENTRYPOINT ["/bin/bash"]
CMD ["python3.7","-m","CEVAC","-x","live", "--loop"]
