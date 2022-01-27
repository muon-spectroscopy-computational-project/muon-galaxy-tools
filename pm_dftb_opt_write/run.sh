#! /bin/bash

set -o errexit

for x in dftb+/* 
do 
    
    if ! out=$(echo $x && cd $x && dftb+)
    then 
    echo 1>&2 "$out"; exit 1
    else
    echo "$out"
    fi
done || exit