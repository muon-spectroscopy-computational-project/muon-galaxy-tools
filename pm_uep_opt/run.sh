#! /bin/bash

set -o errexit

for x in $1/*/*/*.yaml 
do 
    
    if ! out=$(pm-uep-opt $x)
    then 
    echo 1>&2 "$out"; exit 1
    else
    echo "$out"
    fi
done || exit
#pm-uep-opt 