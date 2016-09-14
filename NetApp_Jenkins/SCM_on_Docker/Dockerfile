FROM gitlab/gitlab-ce:latest

COPY swarm-client-2.1-jar-with-dependencies.jar /tmp/swarm-client-2.1-jar-with-dependencies.jar
COPY startcont.sh /usr/bin/startcont.sh

RUN apt-get update
RUN apt-get install -y default-jdk
RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN pip install requests

ENTRYPOINT ["/usr/bin/startcont.sh"] 

