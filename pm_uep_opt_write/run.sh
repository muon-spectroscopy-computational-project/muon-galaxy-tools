for x in $1/*/*/*.yaml 
    do 
        pm-uep-opt $x &&
    done || exit  #pm-uep-opt 