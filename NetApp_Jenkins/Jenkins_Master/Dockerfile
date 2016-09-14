FROM java:8-jdk

#RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
RUN apt-get clean
RUN apt-get update && apt-get install -y git curl zip && rm -rf /var/lib/apt/lists/*
RUN apt-get update
RUN apt-get install -y sudo
RUN apt-get install -y python-pip
RUN pip install requests
RUN pip install texttable

#Docker install
COPY docker.list /etc/apt/sources.list.d/docker.list
RUN apt-get install -y apt-transport-https ca-certificates apt-utils
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y nano
RUN apt-cache policy docker-engine
RUN apt-get install -y docker-engine=1.11.2*
#CMD service docker start 

# nDVP Installation
# download and unpack the application
RUN wget https://github.com/NetApp/netappdvp/releases/download/v1.2.1/netappdvp-1.2.1.tar.gz
RUN tar zxf netappdvp-1.2.1.tar.gz

# move to a location in the bin path
RUN mv netappdvp /usr/local/bin
RUN chown root:root /usr/local/bin/netappdvp
RUN chmod 755 /usr/local/bin/netappdvp

# create a location for the config files
RUN mkdir -p /etc/netappdvp


COPY ontap-nas.json /etc/netappdvp/ontap-nas.json
#CMD netappdvp --config=/etc/netappdvp/ontap-nas.json &

# Jenkins Installation

ENV JENKINS_HOME /var/jenkins_home
ENV JENKINS_SLAVE_AGENT_PORT 50000

ARG user=jenkins
ARG group=jenkins
ARG uid=1000
ARG gid=1000

# Jenkins is run with user `jenkins`, uid = 1000
# If you bind mount a volume from the host or a data container, 
# ensure you use the same uid
RUN groupadd -g ${gid} ${group} \
    && useradd -d "$JENKINS_HOME" -u ${uid} -g ${gid} -m -s /bin/bash ${user}

# Jenkins home directory is a volume, so configuration and build history 
# can be persisted and survive image upgrades
VOLUME /var/jenkins_home

# `/usr/share/jenkins/ref/` contains all reference configuration we want 
# to set on a fresh new installation. Use it to bundle additional plugins 
# or config file with your custom jenkins Docker image.
RUN mkdir -p /usr/share/jenkins/ref/init.groovy.d

RUN mkdir -p /usr/share/jenkins/ref/jobs/Create_User_Workspace_\(NetApp\)
RUN mkdir -p /usr/share/jenkins/ref/jobs/Create_Checkpoint_\(NetApp\)
RUN mkdir -p /usr/share/jenkins/ref/jobs/Delete_Checkpoint_\(NetApp\)
RUN mkdir -p /usr/share/jenkins/ref/jobs/List_Checkpoint_and_Workspace_\(NetApp\)
RUN mkdir -p /usr/share/jenkins/ref/jobs/Create_Local_SCM_\(NetApp\)
RUN mkdir -p /usr/share/jenkins/ref/jobs/Create_Build_Artifact_\(NetApp\)
RUN mkdir -p /usr/share/jenkins/ref/jobs/Zip_and_Copy_Build_Artifact_\(NetApp\)
RUN mkdir -p /usr/share/jenkins/ref/jobs/Delete_User_Workspace_\(NetApp\)
RUN mkdir -p /usr/share/jenkins/ref/jobs/Delete_Build_Artifact_Container_\(NetApp\)
RUN mkdir -p /usr/share/jenkins/ref/jobs/Create_CI_Environment_\(Development_Branch\)_\(NetApp\)
RUN mkdir -p /usr/share/jenkins/ref/jobs/List_StorageTenants_and_Aggregates_\(NetApp\)
RUN mkdir -p /usr/share/jenkins/ref/jobs/List_Volumes_\(NetApp\)
RUN mkdir -p /usr/share/jenkins/ref/jobs/Create_Deployment_File_\(NetApp\)


RUN mkdir -p /tmp/ps
RUN mkdir -p /tmp/vol1
RUN mkdir -p /tmp/vol2

ENV TINI_SHA 066ad710107dc7ee05d3aa6e4974f01dc98f3888

# Use tini as subreaper in Docker container to adopt zombie processes 
RUN curl -fsSL https://github.com/krallin/tini/releases/download/v0.5.0/tini-static -o /bin/tini && chmod +x /bin/tini \
  && echo "$TINI_SHA  /bin/tini" | sha1sum -c -

COPY init.groovy /usr/share/jenkins/ref/init.groovy.d/tcp-slave-agent-port.groovy

COPY Create_CI_Environment_\(Development_Branch\)_\(NetApp\)/ /usr/share/jenkins/ref/jobs/Create_CI_Environment_\(Development_Branch\)_\(NetApp\)
COPY Create_User_Workspace_\(NetApp\)/ /usr/share/jenkins/ref/jobs/Create_User_Workspace_\(NetApp\)
COPY Create_Checkpoint_\(NetApp\)/ /usr/share/jenkins/ref/jobs/Create_Checkpoint_\(NetApp\)
COPY Delete_Checkpoint_\(NetApp\)/ /usr/share/jenkins/ref/jobs/Delete_Checkpoint_\(NetApp\)
COPY List_Checkpoint_and_Workspace_\(NetApp\)/ /usr/share/jenkins/ref/jobs/List_Checkpoint_and_Workspace_\(NetApp\)
COPY Create_Local_SCM_\(NetApp\)/ /usr/share/jenkins/ref/jobs/Create_Local_SCM_\(NetApp\)
COPY Create_Build_Artifact_\(NetApp\)/ /usr/share/jenkins/ref/jobs/Create_Build_Artifact_\(NetApp\)
COPY Zip_and_Copy_Build_Artifact_\(NetApp\)/ /usr/share/jenkins/ref/jobs/Zip_and_Copy_Build_Artifact_\(NetApp\)
COPY Delete_User_Workspace_\(NetApp\) /usr/share/jenkins/ref/jobs/Delete_User_Workspace_\(NetApp\)
COPY Delete_Build_Artifact_Container_\(NetApp\) /usr/share/jenkins/ref/jobs/Delete_Build_Artifact_Container_\(NetApp\)
COPY List_StorageTenants_and_Aggregates_\(NetApp\) /usr/share/jenkins/ref/jobs/List_StorageTenants_and_Aggregates_\(NetApp\)
COPY List_Volumes_\(NetApp\) /usr/share/jenkins/ref/jobs/List_Volumes_\(NetApp\)
COPY Create_Deployment_File_\(NetApp\) /usr/share/jenkins/ref/jobs/Create_Deployment_File_\(NetApp\)


COPY build_artifact_create.py /tmp/ps/build_artifact_create.py
COPY clone_list.py /tmp/ps/clone_list.py
COPY clone_purge.py /tmp/ps/clone_purge.py
COPY Volume_create.py /tmp/ps/Volume_create.py
COPY Volume_create_ba.py /tmp/ps/Volume_create_ba.py
COPY user_workspace_creation.py /tmp/ps/user_workspace_creation.py
COPY scm_config.py /tmp/ps/scm_config.py
COPY CI_dev_branch_create.py /tmp/ps/CI_dev_branch_create.py
COPY Jenkins_slave_create.py /tmp/ps/Jenkins_slave_create.py
COPY snapshot_delete.py /tmp/ps/snapshot_delete.py
COPY snap_show.py /tmp/ps/snap_show.py
COPY snapshot_create.py /tmp/ps/snapshot_create.py
COPY volume_list.py /tmp/ps/volume_list.py
COPY svm_aggr_list.py /tmp/ps/svm_aggr_list.py
COPY build_artifact_container_purge.py /tmp/ps/build_artifact_container_purge.py


ARG JENKINS_VERSION
ENV JENKINS_VERSION ${JENKINS_VERSION:-1.625.16.1}
ARG JENKINS_SHA
ENV JENKINS_SHA ${JENKINS_SHA:-877a3fc0013856795178a7eae4f5357c48d4bf77}

# could use ADD but this one does not check Last-Modified header 
# see https://github.com/docker/docker/issues/8331
RUN curl -fsSL http://jenkins-updates.cloudbees.com/download/je/${JENKINS_VERSION}/jenkins.war -o /usr/share/jenkins/jenkins.war \
  && echo "${JENKINS_SHA}  /usr/share/jenkins/jenkins.war" | sha1sum -c -

ENV JENKINS_UC https://updates.jenkins.io
RUN chown -R ${user} "$JENKINS_HOME" /usr/share/jenkins/ref
# for main web interface:
EXPOSE 8080

# will be used by attached slave agents:
EXPOSE 50000

ENV COPY_REFERENCE_FILE_LOG $JENKINS_HOME/copy_reference_file.log

USER root

COPY cloudbees-referrer.txt /usr/share/jenkins/ref/.cloudbees-referrer.txt
COPY jenkins.sh /usr/local/bin/jenkins.sh
ENTRYPOINT ["/bin/tini", "--", "/usr/local/bin/jenkins.sh"]
# from a derived Dockerfile, can use `RUN plugins.sh active.txt` to setup /usr/share/jenkins/ref/plugins from a support bundle

COPY plugins.sh /usr/local/bin/plugins.sh
COPY plugins.txt /usr/share/jenkins/plugins.txt
RUN /usr/local/bin/plugins.sh /usr/share/jenkins/plugins.txt


