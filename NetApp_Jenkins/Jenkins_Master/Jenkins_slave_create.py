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


import argparse
import sys
import subprocess
from subprocess import call

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-i','--image_name', help='Image to run the container from',dest='image_name',required=True)
    parser.add_argument('-m','--masterip', help='IP address of the Jenkins Master Container',dest='masterip',required=True)
    parser.add_argument('-c','--cont_name', help='Name of the container',dest='cont_name',required=True)
    parser.add_argument('-l','--label_name', help='Name of the label of the slave',dest='label_name',required=True)
    parser.add_argument('-p','--proj_name', help='Name of the project tied to this workspace',dest='proj_name',required=True)
    parser.add_argument('-v','--vol_name', help='Name of the volume tied to this workspace',dest='vol_name',required=True)
    globals().update(vars(parser.parse_args()))
    slave_name = proj_name
    dock_cmd = "docker run -i -t -d -e labelname={} -e masterip={} -e slavename={} --name {} --volume-driver netapp --volume {}:/workspace/{} {}".format(label_name,masterip,slave_name,cont_name,vol_name,proj_name,image_name)
    return_code = subprocess.call(dock_cmd,shell=True)


