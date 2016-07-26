#!/bin/zsh

dir=$1

pair=1
for file in `ls $dir`:
do
    echo $file
    if [ $pair -eq 1 ];
    then
        if [[ $file =~ '(.+)_R[12](.+)' ]];
        then
            basename=$match[1]
            restname=$match[2]
            ./mapping.sh ${dir}/$file ${dir}/${basename}_R2$restname
        fi
    pair=2
    elif [ $pair -eq 2 ];
    then
        pair=1
    fi
done

