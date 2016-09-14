FROM ubuntu

COPY build_artifact_exec.py /tmp/build_artifact_exec.py
COPY clone_purge.py /tmp/clone_purge.py
COPY zipForApprenda.py /tmp/zipForApprenda.py

RUN cd /tmp && curl -O http://repo.jenkins-ci.org/releases/org/jenkins-ci/plugins/swarm-client/2.1/swarm-client-2.1-jar-with-dependencies.jar && chmod +x swarm-client-2.1-jar-with-dependencies.jar
RUN apt-get update
RUN apt-get install -y default-jdk
RUN apt-get install -y git
RUN apt-get install -y python
RUN apt-get install -y zip
RUN apt-get install -y maven
RUN apt-get install -y nano
RUN apt-get install -y vim
RUN apt-get install -y python-pip
RUN pip install requests
RUN mkdir /tmp/vol1
RUN mkdir /tmp/vol2

ENTRYPOINT exec java -jar /tmp/swarm-client-2.1-jar-with-dependencies.jar -name $slavename -master $masterip -labels $labelname -disableClientsUniqueId -mode exclusive 

