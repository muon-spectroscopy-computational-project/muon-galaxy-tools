for x in $1/*/*/*.yaml 
    do 
    output=$(pm-uep-opt $x)
    if echo "$output" | grep -iq 'Error' 
    then 
        >&2 echo "pm-uep-opt failed: $output" 
        exit 2  
    else 
        echo "pm-uep-opt successful: $output" 
    fi
    done #pm-uep-opt 