#!/bin/sh
# Usage tshark2es.sh  <tag>
tshark -T ek -r - | tshark2es.py $1
