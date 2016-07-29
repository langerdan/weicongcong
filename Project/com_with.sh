#!/bin/zsh

com_line=$1
with_obj=$2

for file in `eval $with_obj`
do
    file_basename=$(basename $file)
    if [ $# -eq 2 ];
    then
        echo "=>Command: $com_line $file"
        eval $com_line $file
    elif [ $# -eq 3 ];
    then
        o_flag=$3
        if [[ $o_flag =~ '([\+\-])(.+)' ]];
        then
            direction=$match[1]
            tag=$match[2]
            if [ $di_tri =~ '\+' ];
            then
                echo "=>Command: $com_line $file >${file_basename}${tag}"
                eval $com_line $file >${file_basename}${tag}
            else
                if [[ $file_basename =~ '^(.+)$tag' ]];
                then
                    file_o_name=$match[1]
                    echo "=>Command: $com_line $file >${file_o_name}"
                    eval $com_line $file >${file_o_name}
                fi
            fi
        fi
    else
        echo "**ERROR** in arguments number! got $#, need 2 or 3!"
    fi
done