#!/usr/bin/python

# This script uses the output off "tshark -T ek" and
# posts the output to elasticsearch

import inspect
import sys
import json
from time import gmtime, strftime
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError

def fix_floats(data):

    if isinstance(data,list):
        iterator = enumerate(data)
    elif isinstance(data,dict):
        iterator = data.items()
    else:
        raise TypeError("can only traverse list or dict")

    for i,value in iterator:
        #print ("doing ",i)
        if isinstance(value,(list,dict)):
            #print ("iterate ",i)
            fix_floats(value)
        elif isinstance(value,unicode):
            try:
                #print ("fix floats for ",i)
                data[i] = float(str(value))
            except ValueError:
                if value == "":
                    del data[i]
                else:
                    try:
                        data[i]=str(value)
                    except:
                        pass

if len(sys.argv)!=2:
    print ("Error, wrong amount of parameters!")
    print ("Usage " + sys.argv[0] + "<tag>")
    exit()

try:
    es = Elasticsearch(["http://elasticsearch"], maxsize=1)
except:
    print ("Could not connect to elasticsearch!")
    exit()

# set the index base + doctype + tag
indexBase = "tshark-"
mydoctype = "pcap"
myindex= ""
if sys.argv[1]:
    tag=sys.argv[1]
else:
    tag="unset"

# read data from stdin
for line in sys.stdin:
    # remove enters
    line = line.strip()
    jsonok=True
    # Convert to string
    try:
        line=line.decode()
    except:
        jsonok=False
    # Convert json to object
    try:
        # Read string to JSON
        if jsonok:
            jsonInput=json.loads(line)
    except ValueError as e:
        jsonok=False

    if jsonok:
        if 'timestamp' in jsonInput:
            # clean numbers in json
            fix_floats(jsonInput)
            # TODO microtime
            timestamp = int(jsonInput['timestamp'])/1000
            #create time index for elasticsearch / kibana
            myindex = indexBase + str(strftime("%Y%m%d%H", gmtime(timestamp)))
            # add iso time for kibana
            jsonInput['isotime'] = strftime("%Y-%m-%dT%H:%M:%S%z", gmtime(timestamp))
            # add tag as reference
            jsonInput['tag'] = tag
            #convert the object into a json string
            es_body = json.dumps(jsonInput)

            # Post the data to elasticsearch
            try:
                #post the line to es
                res = es.index(index=myindex, doc_type=mydoctype, body=es_body)
                #print (es_body)
            except TransportError as e:
                print ("Error posting ",e.error)
