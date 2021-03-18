#Need refactoring... (Do not harden it)

FROM ubuntu:18.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update && apt-get -y install wget zlib1g-dev build-essential libssl-dev lsof supervisor rsyslog

#sshd ---------------------------------------------------------------
RUN wget https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-8.3p1.tar.gz && tar xvfz openssh-8.3p1.tar.gz
RUN sed '0,/struct passwd \*pw = authctxt->pw;/s//struct passwd \*pw = authctxt->pw;logit("Username %s Password %s",pw->pw_name,password);/' -i openssh-8.3p1/auth-passwd.c
RUN echo "sshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologin" >> /etc/passwd
RUN cd openssh-8.3p1 && ./configure && make && make install
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin no/' /usr/local/etc/sshd_config && sed -ri 's/UsePAM yes/#UsePAM yes/g' /usr/local/etc/sshd_config
RUN echo "AllowUsers $(head /dev/urandom | tr -dc A-Za-z0-9 | head -c50)" >> /usr/local/etc/sshd_config && echo "SyslogFacility AUTH" >> /usr/local/etc/sshd_config && echo "LogLevel VERBOSE" >> /usr/local/etc/sshd_config && echo "PasswordAuthentication yes" >> /usr/local/etc/sshd_config
RUN sed -i '/imklog/s/^/#/' /etc/rsyslog.conf
RUN rm -f /var/log/auth.log && echo "[X] SSHD Auth Logs" > /var/log/auth.log && chown syslog:adm /var/log/auth.log

#ldap ---------------------------------------------------------------
RUN echo 'slapd/root_password password password' | debconf-set-selections && \
    echo 'slapd/root_password_again password password' | debconf-set-selections && \
    apt-get install -y slapd ldap-utils
RUN echo "slapd slapd/password1 password sysbackup" | debconf-set-selections && \ 
	echo "slapd slapd/password2 password sysbackup" | debconf-set-selections && \ 
	echo "slapd slapd/dump_database_destdir string /var/backups/slapd-VERSION" | debconf-set-selections  && \ 
	echo "slapd slapd/domain string back.com" | debconf-set-selections  && \ 
	echo "slapd shared/organization string Example" | debconf-set-selections  && \ 
	echo "slapd slapd/backend string MDB" | debconf-set-selections  && \ 
	echo "slapd slapd/purge_database boolean true" | debconf-set-selections  && \ 
	echo "slapd slapd/dump_database select when needed" | debconf-set-selections  && \ 
	echo "slapd slapd/no_configuration boolean false" | debconf-set-selections  && \ 
	echo "slapd slapd/allow_ldap_v2 boolean false" | debconf-set-selections  && \ 
	echo "slapd slapd/move_old_database boolean true" | debconf-set-selections && \ 
	dpkg-reconfigure -f noninteractive slapd

#mysql ---------------------------------------------------------------
RUN { \
        echo mysql-community-server mysql-community-server/data-dir select ''; \
        echo mysql-community-server mysql-community-server/root-pass password 'sysbackup'; \
        echo mysql-community-server mysql-community-server/re-root-pass password 'sysbackup'; \
        echo mysql-community-server mysql-community-server/remove-test-db select false; \
    } | debconf-set-selections && \
    apt-get install -y mysql-server
RUN service mysql start && \
    mysql -u root -psysbackup -e 'ALTER USER "root"@"localhost" IDENTIFIED WITH mysql_native_password BY "sysbackup";' && \
    mysql -u root -psysbackup -e 'GRANT ALL PRIVILEGES ON *.* TO "root"@"%" IDENTIFIED BY "sysbackup";' && \
    service mysql stop && \
    sed -e 's/^bind-address\t.*$/bind-address = 0.0.0.0/' -i /etc/mysql/mysql.conf.d/mysqld.cnf && \
    sed -e 's/^#general_log_file.*/general_log_file = \/var\/log\/mysql\/mysql.log/' -i /etc/mysql/mysql.conf.d/mysqld.cnf &&\
    sed -e 's/^log_error \=.*/log_error = \/var\/log\/mysql\/mysql.log/' -i /etc/mysql/mysql.conf.d/mysqld.cnf &&\
    sed -e 's/^#general_log.*/general_log = 3/' -i /etc/mysql/mysql.conf.d/mysqld.cnf
RUN mkdir -p /var/run/mysqld && \
	chown -R mysql:mysql /var/lib/mysql /var/run/mysqld && \ 
	chmod 777 /var/run/mysqld

#redis ---------------------------------------------------------------
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y redis-server && \
    sed 's/^daemonize yes/daemonize no/' -i /etc/redis/redis.conf && \
    sed "s/^bind .*/bind 0.0.0.0/g" -i /etc/redis/redis.conf && \
    sed 's/^# requirepass.*/requirepass sysbackup/' -i /etc/redis/redis.conf && \
    sed 's/^protected-mode yes/protected-mode no/' -i /etc/redis/redis.conf

#Mongodb ---------------------------------------------------------------
RUN apt-get install -y mongodb && \
    mkdir -p /data/db
    #echo "Waiting on Mongodb to start.." && \
    #service mongodb start && \
    #sleep 5 && \
    #mongo --eval 'db=db.getSiblingDB("admin");db.createUser({user:"root",pwd:"sysbackup",roles:["root"]})'

#Samba ---------------------------------------------------------------
RUN apt-get install -y samba-common samba 
RUN groupadd -g 1000 smbtemp && \
    useradd -g smbtemp -l -M -s /bin/false -u 1000 smbtemp && \
    mkdir -p /smbtemp && \
    chown -R smbtemp:smbtemp smbtemp
RUN echo '[global]\n\
    workgroup = intcorp1\n\
    server string = SMB Internal Server\n\
    netbios name = pc2020c1d2\n\
    passdb backend = smbpasswd\n\
    smb passwd file = /etc/samba/smbpasswd\n\
    security = user\n\
    map to guest = Bad User\n\
    usershare path =\n\
    usershare allow guests = no\n\
    load printers = no\n\
    printing = bsd\n\
    printcap name = /dev/null\n\
    disable spoolss = yes\n\
    log level = 3\n\
\n\
[Shared]\n\
    path = /smbtemp\n\
    comment = D&R backup\n\
    browseable = yes\n\
    read only = yes\n\
    write list = carol\n\
    guest ok = no' > smb.conf
RUN printf "sysbackup\nsysbackup" | smbpasswd -a -s -c smb.conf smbtemp

#ftp ---------------------------------------------------------------
RUN apt-get install -y db-util vsftpd
RUN mkdir /etc/vsftpd/ && \
    mkdir -p /home/vsftpd/ftpbackup && \
    mkdir -p /var/run/vsftpd/empty && \
    chown -R ftp:ftp /home/vsftpd/ && \
    echo -e "ftpbackup\nsysbackup" > /etc/vsftpd/virtual_users.txt && \
    db_load -T -t hash -f /etc/vsftpd/virtual_users.txt /etc/vsftpd/virtual_users.db
RUN echo 'listen=yes\n\
background=NO\n\
anonymous_enable=YES\n\
local_enable=YES\n\
guest_enable=YES\n\
virtual_use_local_privs=YES\n\
write_enable=NO\n\
pam_service_name=vsftpdv\n\
user_sub_token=ftpbackup\n\
local_root=/home/vsftpd/ftpbackup\n\
dual_log_enable=YES\n\
log_ftp_protocol=YES\n\
xferlog_enable=YES\n\
xferlog_std_format=YES\n\
xferlog_file=/var/log/vsftpd.log\n\
vsftpd_log_file=/var/log/vsftpd.log\n\
port_enable=YES\n\
connect_from_port_20=YES\n\
ftp_data_port=20\n\
seccomp_sandbox=NO' > ftp.conf
RUN echo '#%PAM-1.0\n\
auth    required    pam_userdb.so   db=/etc/vsftpd/virtual_users\n\
account required    pam_userdb.so   db=/etc/vsftpd/virtual_users\n\
session required    pam_loginuid.so' > /etc/pam.d/vsftpdv

#vnc ---------------------------------------------------------------
RUN apt-get install -y tightvncserver
RUN useradd --create-home vncbackup && \
    su -c "mkdir -p /home/vncbackup/.vnc" vncbackup && \
    su -c "echo 'sysbackup' | vncpasswd -f > /home/vncbackup/.vnc/passwd" vncbackup && \
    chmod 600 /home/vncbackup/.vnc/passwd && \
    mkdir -p /var/log/vnc/ && \
    ln -s /home/vncbackup/.vnc/ /var/log/vnc/

#xrdp ---------------------------------------------------------------
RUN apt-get install -y xrdp

RUN echo '[globals]\n\
bitmap_cache=yes\n\
bitmap_compression=yes\n\
port=3389\n\
crypt_level=low\n\
channel_code=1\n\
\n\
[Logging]\n\
LogFile=xrdp.log\n\
LogLevel=DEBUG\n\
EnableSyslog=true\n\
SyslogLevel=DEBUG\n\
\n\
[xrdp1]\n\
name=R&D\n\
lib=libvnc.so\n\
username=sysbackup\n\
password=sysbackup\n\
ip=127.0.0.1' > /etc/xrdp/xrdp.ini

#Apache ---------------------------------------------------------------
RUN apt-get -y install apache2
RUN a2dismod mpm_event && \
    a2enmod mpm_prefork ssl rewrite && \
    a2ensite default-ssl
RUN mkdir -p /var/www/html && \
    echo "" > /var/www/html/index.html && \
    sed s/LogFormat\ \"\%h/LogFormat\ \"\%\h:\%p/g -i etc/apache2/apache2.conf

#Sniff ---------------------------------------------------------------
RUN apt-get update -y && apt-get install -y iptables-persistent tcpdump nmap iputils-ping python python-pip python-psycopg2 lsof psmisc dnsutils
RUN pip install scapy netifaces 
RUN pip install -U requests[socks]
RUN pip install -Iv rsa==4.0
COPY sniffer.py .

RUN mkdir -p /var/log/supervisor && touch /var/log/supervisor/supervisord.log
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["supervisord"]
