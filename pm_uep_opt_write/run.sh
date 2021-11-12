for x in $1/*/*/*.yaml 
    do 
    pm-uep-opt $x 2> output
    if [ $? != 0 ] 
    then 
        >&2 sed '/^s2/r output' <<< echo "pm-uep-opt failed:" 
        exit 2  
    else 
        sed '/^s2/r output' <<< echo "pm-uep-opt successful:" 
    fi
    done #pm-uep-opt 