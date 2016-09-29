#!/bin/zsh

dir_data=$1
dir_output=$2
if [[ $# -lt 3 ]]; then
	reg='ba[im]|vcf|txt'
else
	reg=$3
fi

for dir_name in `ls $dir_data`
do
	path_dir=$1/$dir_name
	if [[ -d $path_dir ]]; then
		for file in `ls $path_dir`
		do
			if [[ $file =~ "\.(:?$reg)$" ]]; then
				echo "\033[1;36mcopy data: $file to $dir_output\033[0m"
				rsync --info=progress2 $path_dir/$file $dir_output/$file
			else
				echo "\033[1;30m*PASS* $file\033[0m"
			fi
		done
	fi
done
doneReminder "pull data from outbox: complete!"