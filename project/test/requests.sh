#!/usr/bin/env bash
if [ ! -n "$3" ] || [ ! -n "$2" ] || [ ! -n "$1" ]; then
    echo "Usage: $0 fileWithWords ItersCount delayBetweenRequests"
    exit 0
fi

echo "Input: $0 $1 $2 $3"
url="localhost:5000"
IFS=$'\n'
time=$3

for iter in $(seq 1 $2); do
    for word in $(cat $1); do
            d=$(date -d "-3 days" +%s)
            curl -d "data=$word(Старое)&lifeTime=$d" -X POST $url
            sleep $time
            d=$(date -d "+3 days" +%s)
            curl -d "data=$word(Новое)&lifeTime=$d" -X POST $url
            sleep $time
        done
done
