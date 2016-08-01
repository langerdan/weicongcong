#!/bin/zsh

com_line=$1
with_obj=$2
if [ $# -eq 3 ];
    then
    o_flag=$3
    if [[ $o_flag =~ '^([\+\-])(.+)$' ]]; then
        direction=$match[1]
        tag=.$match[2]
    elif [[ $o_flag =~ '^([\+\-])$' ]]; then
        direction=$match[1]
        tag=''
    fi
fi

for file in `eval $with_obj`
do
    file_basename=$(basename $file)
    if [ $# -eq 2 ]; then
        echo "=>Command: $com_line $file"
        eval $com_line $file
    elif [ $# -eq 3 ]; then
        if [[ $direction =~ '\+' ]]; then
            echo "=>Command: $com_line $file >${file_basename}${tag}"
            eval $com_line $file '>'${file_basename}${tag}
        elif [[ $direction =~ '\-' ]]; then
            if [[ $file_basename =~ "^(.+)$tag" ]]; then
                file_o_name=$match[1]
                echo "=>Command: $com_line $file >${file_o_name}"
                eval $com_line $file '>'${file_o_name}
            fi
        else
            echo "**ERROR** incorrect direction flag! got $direction, accept + or -!"
        fi
    else
        echo "**ERROR** incorrect arguments number! got $#, need 2 or 3!"
    fi
done
