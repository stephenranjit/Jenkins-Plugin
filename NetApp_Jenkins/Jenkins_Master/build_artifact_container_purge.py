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
import requests
import subprocess
from subprocess import call

requests.packages.urllib3.disable_warnings()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-cnt','--cont', help='Name of the Container on which workspace is mounted',dest='cont',required=False)
    globals().update(vars(parser.parse_args()))
    dock_cmd = "docker rm -f {}".format(cont)
    return_code = subprocess.call(dock_cmd,shell=True)
    print "Temporary container deleted successfully"

