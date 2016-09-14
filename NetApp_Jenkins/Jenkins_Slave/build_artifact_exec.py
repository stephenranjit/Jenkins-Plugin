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
import subprocess
from datetime import datetime
from subprocess import call



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    #parser.add_argument('-mv','--mntvol', help='Mount path of volume',dest='mntvol',required=True)
    #parser.add_argument('-mc','--mntclone', help='Mount path of the clone',dest='mntclone',required=True)
    mntvol = "/tmp/vol1"
    mntclone= "/tmp/vol2"
    parser.add_argument('-z','--zfile', help='Name of the zipfile',dest='zfile',required=True)
    globals().update(vars(parser.parse_args()))
    i = datetime.now()
    foldertime=i.strftime('%Y_%m_%d_%H:%M_')
    zfile=foldertime+zfile
    zip_cmd = "zip -r {}/{} {}".format(mntclone,zfile,mntclone)
    return_code = subprocess.call(zip_cmd,shell=True)
    own_cmd = "chmod +x {}/{}".format(mntclone,zfile)
    return_code = subprocess.call(own_cmd,shell=True)
    mv_cmd = "mv {}/{} {}".format(mntclone,zfile,mntvol)
    return_code = subprocess.call(mv_cmd,shell=True)
    print "Contents of baseline zipped and archived successfully" 
