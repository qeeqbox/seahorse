<p align="center"> <img src="https://raw.githubusercontent.com/qeeqbox/seahorse/master/readme/seahorselogo.png"></p>

#
[![Generic badge](https://img.shields.io/badge/dynamic/json.svg?url=https://raw.githubusercontent.com/qeeqbox/seahorse/master/info&label=version&query=$.version&colorB=blue)](https://github.com/qeeqbox/seahorse/blob/master/changes.md) [![Generic badge](https://img.shields.io/badge/dynamic/json.svg?url=https://raw.githubusercontent.com/qeeqbox/seahorse/master/info&label=docker-compose&query=$.dockercompose&colorB=green)](https://github.com/qeeqbox/seahorse/blob/master/changes.md)

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

Wait ~2-10 mins until the web browser opens up (until seahorse_initializer_1 exit with 0)

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
- https://www.elastic.co/guide/index.html
- https://scapy.readthedocs.io/en/latest/
- Please let me know if i missed a resource or dependency

## Other Licenses
By using this framework, you are accepting the license terms of each package listed below:
- https://www.elastic.co/downloads/elasticsearch
- https://www.elastic.co/downloads/logstash
- https://www.elastic.co/downloads/kibana
- https://www.elastic.co/downloads/beats/filebeat
- https://www.openbsd.org/policy.html
- https://www.gnu.org/philosophy/free-sw
- https://en.wikipedia.org/wiki/Zlib_License
- https://github.com/chef-boneyard/build-essential/blob/master/LICENSE
- https://packages.debian.org/sid/libssl-dev
- https://kb.acronis.com/system/files/content/2010/02/8220/lsof.txt
- http://supervisord.org/
- https://www.rsyslog.com/doc/v8-stable/licensing.html
- https://www.openldap.org/software/release/license.html
- https://www.mysql.com/about/legal/licensing/oem/
- https://redis.io/topics/license
- https://www.mongodb.com/community/licensing
- https://en.wikipedia.org/wiki/Samba_(software)
- https://en.wikipedia.org/wiki/Vsftpd
- https://github.com/vladmihalcea/db-util
- https://www.tightvnc.com/licensing-tvnserver.php
- https://github.com/neutrinolabs/xrdp/blob/devel/COPYING
- https://www.apache.org/licenses/LICENSE-2.0
- https://packages.debian.org/sid/iptables-persistent
- https://www.tcpdump.org/license.html
- https://nmap.org/npsl/
- https://packages.debian.org/search?keywords=iputils-ping
- https://docs.python.org/3/license.html
- https://en.wikipedia.org/wiki/Pip_(package_manager)
- https://www.psycopg.org/license/
- https://gitlab.com/psmisc/psmisc
- https://github.com/tutumcloud/dnsutils/blob/master/LICENSE
- https://github.com/python-ldap/python-ldap/blob/master/LICENCE
- https://github.com/FreeRDP/FreeRDP/blob/master/LICENSE
- http://net-tools.sourceforge.net/
- https://github.com/kevinburke/sshpass/blob/master/LICENSE
- https://github.com/paramiko/paramiko/blob/master/LICENSE
- https://dev.mysql.com/doc/dev/connector-python/8.0/license.html
- https://github.com/mongodb/mongo-python-driver/blob/master/LICENSE
- https://miketeo.net/blog/projects/pysmb
- https://github.com/sibson/vncdotool/blob/main/LICENSE.txt
- https://github.com/psf/requests/blob/master/LICENSE
- https://github.com/pyca/cryptography/blob/master/LICENSE

## Disclaimer\Notes
- Remember to change the passwords
