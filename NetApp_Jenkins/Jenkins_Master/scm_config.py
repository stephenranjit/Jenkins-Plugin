################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp
#          technologies.  This script is not officially supported as a
#          standard NetApp product.
#
# Purpose: Script to create a new container running GOGS with a NetApp volume mounted.
#
#
# Usage:   %> scm_config.py <args>
#
# Author:  Vishal Kumar S A (vishal.kumarsa@netapp.com)
#          Akshay Patil (akshay.patil@netapp.com)
#          Shrivatsa Upadhye (shrivatsa.upadhye@netapp.com)
#
# NETAPP CONFIDENTIAL
# -------------------
# Copyright 2016 NetApp, Inc. All Rights Reserved.
#
# NOTICE: All information contained herein is, and remains the property
# of NetApp, Inc.  The intellectual and technical concepts contained
# herein are proprietary to NetApp, Inc. and its suppliers, if applicable,
# and may be covered by U.S. and Foreign Patents, patents in process, and are
# protected by trade secret or copyright law. Dissemination of this
# information or reproduction of this material is strictly forbidden unless
# permission is obtained from NetApp, Inc.
#
################################################################################
import argparse
import sys
import subprocess
from subprocess import call
import base64
import random
import requests
import ssl
import time
import os

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
    #"security_user_id":uid,
    #"security_group_id":gid,
    "junction_path":'/'+vol_name,
    "security_permissions":"777",
    "is_snap_dir_access_enabled":"False"
    }
    r = requests.post(url, headers=headers,json=data, verify=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-v','--vol_name', help='Name of the volume tied to this workspace',dest='vol_name',required=True)
    parser.add_argument('-vs','--vs name', help='Select SVM',dest='svm_name',required=True)
    parser.add_argument('-s','--vol_size', help='Size of Volume',dest='vol_size',required=True)
    parser.add_argument('-ag','--aggr_name', help='Aggregate to create or clone from',dest='aggr_name',required=True)
    parser.add_argument('-a','--api', help='API server IP:port',dest='api',required=True)
    parser.add_argument('-uid','--uid', help='Add User ID',dest='uid')
    parser.add_argument('-gid','--gid', help='Add Group ID',dest='gid')
    parser.add_argument('-c','--cont_name', help='Name of the container',dest='cont_name',required=True)
    parser.add_argument('-apiuser','--apiuser', help='Add APIServer Username',dest='apiuser',required=True)
    parser.add_argument('-apipass','--apipass', help='Add APIServer Password',dest='apipass',required=True)
    parser.add_argument('-m','--masterip', help='URL of Jenkins Master',dest='masterip',required=True)
    parser.add_argument('-ip','--hostip', help='IP Address of the Host',dest='hostip',required=True)

    globals().update(vars(parser.parse_args()))
    randvalInt  = str(random.randint(1,65535))
    label_name = cont_name
    slave_name = cont_name
    vol_name = vol_name + "_SCM_" + randvalInt
    count = 0
    make_volume(vol_name,aggr_name,svm_name,vol_size)
    while check_vol(vol_name) == False:
        time.sleep(1)
        count=count+1
    print "New Local repo volume created successfully in {} seconds".format(count)
    
    config_vol_name = vol_name + '_config'
    config_vol_size = 51200
    count = 0
    make_volume(config_vol_name,aggr_name,svm_name,config_vol_size)
    while check_vol(config_vol_name) == False:
        time.sleep(1)
        count=count+1
    print "New Local config volume created successfully in {} seconds".format(count)

       
    logs_vol_name = vol_name + '_logs'
    logs_vol_size = 51200
    count = 0 
    make_volume(logs_vol_name,aggr_name,svm_name,logs_vol_size)
    while check_vol(logs_vol_name) == False:
        time.sleep(1)
        count=count+1
    print "New Local log volume created successfully in {} seconds".format(count)

    dock_cmd = "docker run --detach --name {} --hostname {} --restart always -p 10022:22 -p 80:80 -p 443:443  -e labelname={} -e masterip={} -e slavename={} --volume-driver netapp --volume {}:/etc/gitlab --volume {}:/var/log/gitlab --volume {}:/var/opt/gitlab devopsnetapp/netapp-jenkins_gitlab".format(cont_name,hostip,label_name, masterip, slave_name,config_vol_name,logs_vol_name,vol_name)
    return_code = subprocess.call(dock_cmd,shell=True)
