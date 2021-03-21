from paramiko import SSHClient, AutoAddPolicy, util, MissingHostKeyPolicy
from ldap import open as lopen
from redis import Redis
from mysql.connector import connect as mysqlconnect
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from smb.SMBConnection import SMBConnection
from ftplib import FTP
from vncdotool import api as vncapi
from subprocess import Popen, PIPE
from time import sleep
from sys import stdout
from requests import post, get
from requests.auth import HTTPBasicAuth
from os import walk, path
from urllib3 import disable_warnings, exceptions

disable_warnings(exceptions.InsecureRequestWarning)
util.log_to_file("/var/log/paramiko_tmp.log")

username = 'elastic'
password = 'changeme'
host_l = 'logstash'
host_k = 'kibana'
host_h = 'honeypot'
password_h = 'dummy'

res = True


def wait_for_logstash(host):
    while True:
        try:
            res = get('http://{}:9600'.format(host), timeout=3)
            if res.status_code == 200:
                print("Logstash is Running")
                return True
        except BaseException:
            pass

        print("Logstash is initializing -- Waiting 10 sec")
        stdout.flush()
        sleep(10)


def wait_for_kibana(host):
    while True:
        try:
            res = get('http://{}:5601'.format(host), timeout=3)
            if res.status_code == 200:
                print("Kibana is Running")
                return True
        except BaseException:
            pass

        print("Kibana is initializing -- Waiting 10 sec")
        stdout.flush()
        sleep(10)


def test_ssh(host, password):
    print("Testing SSH")
    try:
        process = Popen(["sshpass", "-p", password, "ssh", "-o", "StrictHostKeyChecking=no", "{}@{}".format("test", host)], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        #ssh = SSHClient()
        # util.log_to_file("filename.log")
        # ssh.set_missing_host_key_policy(MissingHostKeyPolicy())
        #ssh.connect(host, username="root", password=password)
    except Exception as e:
        pass


def test_ldap(host, password):
    print("Testing LDAP")
    try:
        l = lopen(host=host, port=389)
        l .simple_bind_s("cn=admin,dc=example,dc=com", password)
    except Exception as e:
        pass


def test_redis(host, password):
    print("Testing REDIS")
    try:
        r = Redis(host=host, port=6379, password=password)
        r.ping()
    except Exception as e:
        pass


def test_mysql(host, password):
    print("Testing MYSQL")
    try:
        cnx = mysqlconnect(host=host, user='root', password=password)
        cnx.is_connected()
    except Exception as e:
        pass


def test_mongo(host, password):
    print("Testing MONGO")
    try:
        client = MongoClient("mongodb://root:{}@{}:27017/admin".format(password, host))
        client.admin.command('ismaster')
    except Exception as e:
        pass


def test_smb(host, password):
    print("Testing SMB")
    try:
        conn = SMBConnection("smbtemp", password, "test", "INTCORP1")
        conn.connect(host, 445)
        files = conn.listPath('Shared', '/')
        print("test_smb Success")
    except Exception as e:
        pass


def test_ftp(host, password):
    print("Testing FTP")
    try:
        server = FTP()
        server.connect(host, 21)
        server.login('test', password)
        server.dir()
    except Exception as e:
        pass


def test_vnc(host, password):
    print("Testing VNC")
    try:
        client = vncapi.connect(host, password=password)
        client.timeout = 5
        client.keyPress('enter')
    except Exception as e:
        pass


def test_rdp(host, password):
    print("Testing RDP")
    try:
        process = Popen(['xfreerdp', '--ignore-certificate', '--authonly', '-u', 'user', '-p', 'pass', host], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
    except Exception as e:
        pass


def test_web(host, password):
    print("Testing HTTP & HTTPS")
    try:
        get('http://{}'.format(host), timeout=3)
        get('https://{}'.format(host), timeout=3, verify=False)
    except Exception as e:
        pass


def init():
    print("Initializing started")
    if wait_for_logstash(host_l):

        test_ssh(host_h, password_h)
        test_ldap(host_h, password_h)
        test_mysql(host_h, password_h)
        test_redis(host_h, password_h)
        test_mongo(host_h, password_h)
        test_smb(host_h, password_h)
        test_ftp(host_h, password_h)
        test_vnc(host_h, password_h)
        test_rdp(host_h, password_h)
        test_web(host_h, password_h)

        if wait_for_kibana(host_k):
            file = "backup.ndjson"
            try:
                r = post("http://{}:5601/api/saved_objects/_import".format(host_k), headers={'kbn-xsrf': 'true'}, files={'file': open(file, 'r')}, auth=HTTPBasicAuth(username, password))
                if r.status_code == 200:
                    print("Importing {} OK".format(file))
                    return True
                else:
                    print("Importing {} Failed, please restart the process...".format(file))
            except Exception as e:
                print("Importing {} Failed, something wrong..".format(file))


if init():
    print("Initializing Done!")
else:
    print("Initializing Failed")
