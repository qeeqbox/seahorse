<p align="center"> <img src="https://raw.githubusercontent.com/qeeqbox/seahorse/master/readme/seahorselogo.png"></p>

#
[![Generic badge](https://img.shields.io/badge/dynamic/json.svg?url=https://raw.githubusercontent.com/qeeqbox/seahorse/master/info&label=version&query=$.version&colorB=blue&style=flat-square)](https://github.com/qeeqbox/seahorse/blob/master/changes.md) [![Generic badge](https://img.shields.io/badge/dynamic/json.svg?url=https://raw.githubusercontent.com/qeeqbox/seahorse/master/info&label=docker-compose&query=$.dockercompose&colorB=green&style=flat-square)](https://github.com/qeeqbox/seahorse/blob/master/changes.md) [![Generic badge](https://img.shields.io/static/v1?label=%F0%9F%91%8D&message=Thank%20You%20For%20The%20Support!!&color=yellow&style=flat-square)](https://github.com/qeeqbox/woodpecker/stargazers)

ELKFH (Elastic, Logstash, Kibana, Filebeat and Honeypot) system for monitoring security tools that interact with (HTTP, HTTPS, SSH, RDP, VNC, Redis, MySQL, MONGO, SMB, LDAP)

## Kibana Interface
<img src="https://raw.githubusercontent.com/qeeqbox/seahorse/master/readme/intro.gif" style="max-width:768px"/>

## General Features
- Logs are accessible via Kibana
- All services running in one container using supervisord
- Ingress sniffer, layers and packet parser

## Install and run
#### On Ubuntu 18 or 19 System (Auto-configure)
```bash
git clone https://github.com/qeeqbox/seahorse.git
cd seahorse
chmod +x ./run.sh
./run.sh auto_configure

Wait ~2-10 mins until the web browser opens up (until seahorse_initializer_1 exit with 0) - username is elastic and password is changeme

```

## Current Servers
- HTTP (Apache)
- HTTPS (Apache)
- SSH (Custom OpenSSH)
- FTP (vsftpd)
- SMB (samba)
- ldap (slapd)
- VNC (tightvncserver)
- RDP (xrdp)
- Redis (redis-server)
- Mysql (mysql-community-server)

## Changes
- 2020.V.01.01

## Roadmap
- Add more services

## Resources
`elastic, scapy`

## Other Licenses
By using this framework, you are accepting the license terms of all these packages: `elasticsearch, logstash, kibana, filebeat, openbsd, openbsd, Zlib, build-essential, libssl-dev, lsof, supervisord, rsyslog, openldap, mysql, redis, mongodb, Samba, Vsftpd, db-util, tvnserver, xrdp, apache, iptables, tcpdump, nmap, iputils-ping, python, Pip, psycopg, psmisc, dnsutils, python-ldap, FreeRDP, net-tools, sshpass, paramiko, connector-python, mongo-python-driver, pysmb, vncdotool, requests, cryptography`


## Disclaimer\Notes
- Do not deploy without proper configuration
- Setup some security group rules and remove default credentials
- Please let me know if i missed a resource or dependency
