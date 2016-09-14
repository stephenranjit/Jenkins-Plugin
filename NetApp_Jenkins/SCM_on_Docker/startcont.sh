#!/bin/bash

set -e

exec java -jar /tmp/swarm-client-2.1-jar-with-dependencies.jar -name $slavename -master $masterip -labels $labelname -disableClientsUniqueId -mode exclusive &


bash /assets/wrapper 

