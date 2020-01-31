#! /bin/sh

apt-get update && apt-get install unixodbc unixodbc-dev curl openssh-server rsync alien dpkg-dev debhelper build-essential libaio1 -y 
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/18.10/prod.list > /etc/apt/sources.list.d/mssql-release.list && apt-get update 
cd /root && curl https://download.oracle.com/otn_software/linux/instantclient/195000/oracle-instantclient19.5-basiclite-19.5.0.0.0-1.x86_64.rpm > oracle.rpm && alien --scripts oracle.rpm && dpkg -i *.deb
ACCEPT_EULA=Y apt-get install msodbcsql17 -y
apt-get install python3.8 python3-pip python3.8-dev -y && python3.8 -m pip install pip --upgrade
pip3 install pandas pandasql sqlalchemy pyodbc cx_Oracle pyyaml paramiko requests croniter jinja2 flask gunicorn django
ln -s /usr/bin/python3.8 /usr/bin/python && ln -s /usr/bin/pip3 /usr/bin/pip

