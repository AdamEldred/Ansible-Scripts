#!/usr/bin/env python

"""Local network discovery inventory script
Generates an Ansible inventory of all hosts on a local network
set environmet variables in source, ex:

target_network: 127.0.0.1/24
target_port: 22


Requires nmap and socket on task server.  For AWX I used:
docker ps 

docker exec -i -t <awx_task container id> /bin/bash 

/var/lib/awx/venv/ansible/bin/pip install python-nmap 

/var/lib/awx/venv/ansible/bin/pip install websocket 

Yum install nmap 
"""

import argparse
import json
import nmap
import socket
import time
import os

class LocalNetworkInventory(object):
  def __init__(self):
    """Main execution path"""
    data_to_print = ""
    data_to_print = self.json_format_dict(self.get_inventory())
    print(data_to_print)

  def get_inventory(self):
    """Populate `self.inventory` with hosts."""
    return { "all": { "hosts": self.lookup_local_ips() }}

  def json_format_dict(self, data):
    return json.dumps(data, sort_keys=True, indent=2)

  def lookup_local_ips(self):
    """Lookup IPs of hosts connected to the local network"""
    nm = nmap.PortScanner()
    nm.scan(hosts=os.environ.get("target_network"), arguments="-p {} --open".format(os.environ.get("target_port")))
    return nm.all_hosts()

LocalNetworkInventory()