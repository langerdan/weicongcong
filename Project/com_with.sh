#!/bin/zsh

com_line=$1
with_obj=$2
if [ $# -eq 3 ];
    then
    operations=$3
    redi_flag=''
    if [[ $operations =~ '^>(.+)$' ]]; then
        operations=$match[1]
        redi_flag='>'
    fi
    if [[ $operations =~ '^([+])(.+)$' ]]; then
        mod_flag=$match[1]
        tag=.$match[2]
    elif [[ $operations =~ '^([-=])$' ]]; then
        mod_flag=$match[1]
        tag=''
    elif [[ $operations =~ '^([#])(.+)#(.+)$' ]]; then
        mod_flag=$match[1]
        tag_ori=$match[2]
        tag_mod=$match[3]
    fi
fi

for file in `eval $with_obj`
do
    file_basename=$(basename $file)
    if [ $# -eq 2 ]; then
        echo "=>Command: $com_line $file"
        eval $com_line $file
    elif [ $# -eq 3 ]; then
        if [[ $mod_flag =~ '\+' ]]; then
            echo "=>Command: $com_line $file ${redi_flag}${file_basename}${tag}"
            eval $com_line $file ${redi_flag}${file_basename}${tag}
        elif [[ $mod_flag =~ '\-' ]]; then
            if [[ $file_basename =~ "^(.+)\.[^.]+$" ]]; then
                file_o_name=$match[1]
                echo "=>Command: $com_line $file ${redi_flag}${file_o_name}"
                eval $com_line $file ${redi_flag}${file_o_name}
            fi
        elif [[ $mod_flag =~ '\=' ]]; then
            echo "=>Command: $com_line $file ${redi_flag}${file_basename}"
            eval $com_line $file ${redi_flag}${file_basename}
        elif [[ $mod_flag =~ '\#' ]]; then
            if [[ $file_basename =~ "^(.+)$tag_ori" ]]; then
                file_o_name=$match[1]
                echo "=>Command: $com_line $file ${redi_flag}${file_o_name}${tag_mod}"
                eval $com_line $file ${redi_flag}${file_o_name}${tag_mod}
            fi
        else
            echo "**ERROR** incorrect mod flag! got \"$operations\", accept +, - or #!"
        fi
    else
        echo "**ERROR** incorrect arguments number! got $#, need 2 or 3!"
    fi
done
