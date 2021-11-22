#! /bin/bash

set -o errexit

for x in $1/*/*/*.yaml 
    do 
        pm-uep-opt $x &&
    done || exit 1 
    #pm-uep-opt 