#! /bin/bash

set -o errexit

run(){
    if ! out=$(pm-uep-opt $1); then 
        echo 1>&2 "$out"; exit 1
    else
        echo "$out"
    fi
}

pids=()
for x in $1/*/*/*.yaml; do 
    run $x & pids+=($!)
done

declare -i failed=0
for pid in ${pids[@]}; do
    if ! wait $pid; then
        failed+=1
    fi
done

if [ $failed -eq ${#pids[@]} ]; then
    >&2 echo "ERROR: All optimisations failed"
    exit 1
elif [ $failed -eq 0 ]; then
    echo "All optimisations succeeded"
    exit 0
else
    echo "WARNING: $failed optimisation(s) failed"
    exit 0
fi
