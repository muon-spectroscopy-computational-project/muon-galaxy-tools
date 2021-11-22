for x in $1/*/*/*.yaml 
    do 
        pm-uep-opt $x &&
        echo "$?"
    done || exit  #pm-uep-opt 