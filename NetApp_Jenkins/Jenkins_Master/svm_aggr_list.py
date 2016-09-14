
########################################################################################################################
#                                                                                                                      #
# NetApp -Jenkins Plugin using Docker container                                                                        #
# Copyright 2016 NetApp, Inc.                                                                                          #
#                                                                                                                      #
# The python scripts in this folder and others, allow CI admin and the developer a plugin that integrates              #
# with Cloudbees Jenkins Enterprise using NetApp ONTAP APIs to provide an automated continuous Integration (CI)        #
# pipeline using Gitlab, Docker container and persistent storage using NetApp Docker Volume Plugin (nDVP) for ONTAP.   #
#                                                                                                                      #
# Maintained By:  Shrivatsa Upadhye (shrivatsa.upadhye@netapp.com)                                                     #
#                 Akshay Patil (Akshay.Patil@netapp.com)                                                               #
#                                                                                                                      #
########################################################################################################################

import base64
import argparse
import sys
import requests
import ssl
import subprocess
import time
import os
from subprocess import call
import texttable as tt

requests.packages.urllib3.disable_warnings()

def get_volumes():
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')

    url = "https://{}/api/1.0/ontap/volumes/".format(api)
    headers = {
        "Authorization": "Basic %s" % base64string,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    r = requests.get(url, headers=headers,verify=False)
    #print r.json()
    #print "get_volumes works"
    return r.json()

def get_key_svms(svm_name):
    tmp = dict(get_svms())
    svms = tmp['result']['records']
    for i in svms:
        if i['name'] == svm_name:
            # print i
            return i['key']

def get_svms():
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')

    url = "https://{}/api/1.0/ontap/storage-vms/".format(api)
    headers = {
        "Authorization": "Basic %s" % base64string,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    r = requests.get(url, headers=headers,verify=False)
    #print r.json()
    return r.json()

def get_vservers():
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')

    url = "https://{}/api/1.0/ontap/storage-vms/".format(api)
    headers = {
        "Authorization": "Basic %s" % base64string,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    r = requests.get(url, headers=headers,verify=False)
    #print r.json()
    #print "get_vserver works"
    return r.json()

def get_aggr():
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')

    url = "https://{}/api/1.0/ontap/aggregates/".format(api)
    headers = {
        "Authorization": "Basic %s" % base64string,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    r = requests.get(url, headers=headers,verify=False)
    #print r.json()
    #print "get_aggr works"
    return r.json()

def disp_vservers():
    ctr = 0
    tmp = dict(get_vservers())
    vservers = tmp['result']['records']
    tab = tt.Texttable()
    header = ['Vserver name']
    tab.header(header)
    tab.set_cols_align(['c'])
    for i in vservers:
        ctr = ctr + 1
        cl = i['name']
        row = [cl]
        tab.add_row(row)
        tab.set_cols_align(['c'])
    print "Number of Vservers for the NetApp cluster :{}".format(ctr)
    s = tab.draw()
    print s

def disp_aggr():
    ctr = 0
    tmp = dict(get_aggr())
    aggr = tmp['result']['records']
    tab = tt.Texttable()
    header = ['Aggregate name','Total size available in GigaBytes']
    tab.header(header)
    tab.set_cols_align(['c','c'])
    for i in aggr:
        ctr = ctr + 1
        ag = i['name']
	si = i['size_avail']
        si = si/1024/1024/1024
        row = [ag,si]
        tab.add_row(row)
        tab.set_cols_align(['c','c'])
    print "Number of Aggregates for the NetApp cluster:{}".format(ctr)
    s = tab.draw()
    print s

def disp_vol():
    ctr = 0
    tmp = dict(get_volumes())
    vols = tmp['result']['records']
    tab = tt.Texttable()
    header = ['Volume name','Total size available in MegaBytes']
    tab.header(header)
    tab.set_cols_align(['c','c'])
    key = get_key_svms(svm_name)
    for i in vols:
        if i['storage_vm_key'] == key:
            ctr = ctr + 1
            vol = i['name']
	    si = i['size_avail']
	    si = si/1024/1024	
            row = [vol,si]
            tab.add_row(row)
            tab.set_cols_align(['c','c'])
    print "Number of Volumes for this Vserver:{}".format(ctr)
    s = tab.draw()
    print s
	
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-a','--api', help='API server IP:port details',dest='api')
    parser.add_argument('-apiuser','--apiuser', help='Add APIServer Username',dest='apiuser',required=True)
    parser.add_argument('-apipass','--apipass', help='Add APIServer Password',dest='apipass',required=True)
    #parser.add_argument('-vs','--vs name', help='Select SVM',dest='svm_name',required=True)
    globals().update(vars(parser.parse_args()))
    disp_vservers()
    disp_aggr()
    #disp_vol()
