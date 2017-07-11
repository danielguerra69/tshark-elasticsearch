## Tshark output to elasticsearch

![Wireshark](https://www.wireshark.org/assets/theme-2015/images/wireshark_logo@2x.png)

Wireshark is a network packet decoder.

This image contains the wireshark commandline tool,
[tshark](https://www.wireshark.org/docs/man-pages/tshark.html) and a python script that posts the data in
elasticsearch

## Usage

docker-compose

I strongly advise to use [docker-compose](https://docs.docker.com/compose/)

```bash
mkdir tshark-elasticsearch
cd tshark-elasticsearch
wget https://raw.githubusercontent.com/danielguerra69/tshark-elasticsearch/master/docker-compose.yml
docker-compose up -d
```

The compose starts an elasticsearch cluster, kibana and tshark

Copy pcap data to analyze

```bash
docker cp /mydir/mypcap.pcap tshark:/data/pcap
```

Analyze the data

```bash
docker-compose exec tshark bash
tshark -r /data/pcap/mypcap.pcap -T ek | tshark2es.py <mytag>
```

The tag is use to seperate the data, you can use any word.

View the data

Go with your browser to http://<docker-ip>:5601

In kibana use the index tshark-* and isotime
 
