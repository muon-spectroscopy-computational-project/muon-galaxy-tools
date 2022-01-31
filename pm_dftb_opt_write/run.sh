#! /bin/bash

set -o errexit
if [ ! -d "$1/dftb+" ]; then echo "no folder"; else echo "folder"; fi
[ ! -d "$1/dftb+" ] && ( echo 1>&2 "no dftb+ structures found" && exit 2 )
for x in $1/dftb+/* 
do 
    
    if ! out=$(echo $x && cd $x && dftb+)
    then 
    echo 1>&2 "$out"; exit 3
    else
    echo "$out"
    fi
done || exit 