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
    return r.json()

def get_aggrs():
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')

    url = "https://{}/api/1.0/ontap/aggregates/".format(api)
    headers = {
        "Authorization": "Basic %s" % base64string,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    r = requests.get(url, headers=headers,verify=False)
    #print r.json()
    return r.json()


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

def get_size(vol_size):
    tmp = int(vol_size) * 1024 * 1024
    return tmp


def get_key_aggr(aggr_name):
    tmp = dict(get_aggrs())
    aggrs = tmp['result']['records']
    for i in aggrs:
        if i['name'] == aggr_name:
            # print i
            return i['key']

def get_key_svms(svm_name):
    tmp = dict(get_svms())
    svms = tmp['result']['records']
    for i in svms:
        if i['name'] == svm_name:
            # print i
            return i['key']

def check_vol(vol_name):
    tmp = dict(get_volumes())
    vols = tmp['result']['records']
    names = [i['name'] for i in vols]
    #print "Volume Names: ", names
    return vol_name in names

def get_jpath(vol_name):
    tmp = dict(get_volumes())
    vols = tmp['result']['records']
    for i in vols:
         if i['name'] == vol_name:
            # print i
            return i['junction_path']

def make_volume(vol_name,aggr_name,svm_name,vol_size):
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    url = "https://{}/api/1.0/ontap/volumes/".format(api)
    aggr_key=get_key_aggr(aggr_name)
    svm_key=get_key_svms(svm_name)
    v_size=get_size(vol_size)


    headers = {
    "Authorization": "Basic %s" % base64string,
    "Content-Type": "application/json",
    "Accept": "application/json"
    }
    data= {
    "aggregate_key":aggr_key,
    "size":v_size,
    "storage_vm_key":svm_key,
    "name":vol_name,
    "junction_path":'/'+vol_name,
    "security_permissions":"777",
    "is_snap_dir_access_enabled":"False"
    }
    r = requests.post(url, headers=headers,json=data, verify=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-ag','--aggr_name', help='Aggregate to create or clone from',dest='aggr_name',required=True)
    parser.add_argument('-vs','--vs name', help='Select SVM',dest='svm_name',required=True)
    parser.add_argument('-s','--vol_size', help='Size of Volume',dest='vol_size',required=True)
    parser.add_argument('-v','--vol_name', help='Volume to create or clone from',dest='vol_name',required=True)
    parser.add_argument('-a','--api', help='API server IP:port',dest='api',required=True)
    parser.add_argument('-apiuser','--apiuser', help='Add APIServer Username',dest='apiuser',required=True)
    parser.add_argument('-apipass','--apipass', help='Add APIServer Password',dest='apipass',required=True)
    #parser.add_argument('-uid','--uid', help='Add User ID',dest='uid')
    #parser.add_argument('-gid','--gid', help='Add Group ID',dest='gid')
    globals().update(vars(parser.parse_args()))
    count = 0
    make_volume(vol_name,aggr_name,svm_name,vol_size)

    while check_vol(vol_name) == False:
        time.sleep(1)
        count=count+1

    print "New Build artifact archival volume created successfully in {} seconds".format(count)

