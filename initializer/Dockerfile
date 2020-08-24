FROM ubuntu:18.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update && apt-get install -y python-ldap freerdp-x11 python python-pip net-tools sshpass iputils-ping
RUN pip install paramiko redis mysql-connector-python pymongo pysmb vncdotool requests
RUN pip install install cryptography==2.4.2
COPY init.py . 
COPY backup.ndjson .