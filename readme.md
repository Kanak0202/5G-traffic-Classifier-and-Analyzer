# While working on docker

* Follow the commands below if you are working using docker containers *

## In client-server folder

* Make sure to update your mongoDB URI in PacketCapture.py file. Also make sure you have entered the correct interface (eg. eth0) on which you want to capture packets in the tshark command *

* Make sure to modify dockerignore file before making containers to add only necessary files to the container *

* Change connection URL in interface client files for your specific container connection *
 
### For building server-image using server dockerfile
 docker build -t server-image -f Dockerfile.Server .

### For building client-image using client dockerfile
docker build -t client-image -f Dockerfile.Client .

### For building all-clients-image using all-clients dockerfile
docker build -t all-clients-image -f Dockerfile.Client .

### To make a docker network for client and server
docker network create hpe-network

### To run the server-container by giving it admin privilidges for efficient packet capture
 docker run -d --name server-container --cap-add=NET_RAW --cap-add=NET_ADMIN --network hpe-network server-image

### To run the client-container in hpe-network network
docker run -it --name client-container --network hpe-network client-image

### To stop a docker container
 docker stop container_name

### To attach the client-container for giving input through the terminal (Enter the value of the interface to send requests to server)
 docker attach client-container 

### To attach the all-clients-container for giving input through the terminal (Enter s to start sending requests to server, q to quit)
 docker attach all-clients-container 

## In Packet Analyzer folder

* Make sure to update your mongoDB URI and mysql details (user, password, host, port, database, auth_plugin) in PacketAnalysis.py file *

### For building mysql-store-image for analyzing packets and storing analysis in mysql
 docker build -t mysql-store-image -f Dockerfile.MySql .


* To visualize the data on grafana, create grafana container and create a dashboard by entering mysql connection details *

### Running docker container
 docker run -d --name=grafana -p 3000:3000 -v /etc/localtime:/etc/localtime:ro -v /etc/timezone:/etc/timezone:ro grafana/grafana

### Starting same grafana container again (if container stopped)
 docker start grafana

### Run mysql query in grafana

* For bar graph (set time according to your preference, here set to one day), set auto refresh in grafana to preferred rate for live visualization *

SELECT interface, COUNT(*) as count
FROM hpe_packets.keyword_matches
WHERE arrival_time >= NOW() - INTERVAL 86400 SECOND
GROUP BY interface
ORDER BY count DESC;

* For time series graph, add interfaces of your preference. You can also run multiple queries by changing interface name for multiple series *

SELECT
    FROM_UNIXTIME(UNIX_TIMESTAMP(arrival_time) - MOD(UNIX_TIMESTAMP(arrival_time), 5)) AS time,
    interface,
    COUNT(*) AS N7
FROM
    hpe_packets.keyword_matches
WHERE interface="N7"
GROUP BY
    time,
    interface
ORDER BY
    time
LIMIT 50000;

# While working on local system

* Follow the commands below if you are working locally on your system *


## In client-server folder

* Change connection URL in interface client files for your specific connection (eg. http://localhost:8000) *

### Start server
 npm run start

### Start packet capture
* To avoid loss of packets, run this file first *
* Make sure to change the name of the interface you are capturing packets on. To capture packets from localhost, use "Adapter for loopback traffic capture". Also make sure to update the mongoDB URI *

 python PacketCapture.py

### Start client
 python client.py

### Start all-clients
 python allClient.py

### In Packet Analyzer folder
 python runAnalysis.py

* To visualize the data on grafana, install and setup grafana on your local system and create a dashboard by entering mysql connection details *

### Run mysql query in grafana

* For bar graph (set time according to your preference, here set to one day), set auto refresh in grafana to preferred rate for live visualization *

SELECT interface, COUNT(*) as count
FROM hpe_packets.keyword_matches
WHERE arrival_time >= NOW() - INTERVAL 86400 SECOND
GROUP BY interface
ORDER BY count DESC;

* For time series graph, add interfaces of your preference. You can also run multiple queries by changing interface name for multiple series *

SELECT
    FROM_UNIXTIME(UNIX_TIMESTAMP(arrival_time) - MOD(UNIX_TIMESTAMP(arrival_time), 5)) AS time,
    interface,
    COUNT(*) AS N7
FROM
    hpe_packets.keyword_matches
WHERE interface="N7"
GROUP BY
    time,
    interface
ORDER BY
    time
LIMIT 50000;
