#!/bin/zsh

com_line=$1
with_obj=$2
if [[ $# -eq 3 || $# -eq 4 ]]; then
	operations=$3

	redi_flag=''
	if [[ $operations =~ '^%(.+)$' ]]; then
		operations=$match[1]
		redi_flag='>'
	fi

	dir_output=''
	if [[ $operations =~ '^@(.+)@(.+)$' ]]; then
		operations=$match[2]
		dir_output="$match[1]/"
	fi

	if [[ $operations =~ '^([+])(.+)$' ]]; then
		mod_flag=$match[1]
		tag=.$match[2]
	elif [[ $operations =~ '^([-=])' ]]; then
		mod_flag=$match[1]
		tag=''
	elif [[ $operations =~ '^([#])(.+)#(.+)$' ]]; then
		mod_flag=$match[1]
		tag_ori=$match[2]
		tag_mod=$match[3]
	fi

	pipe_out=''
	if [[ $# -eq 4 ]]; then
		pipe_out="| $4"
	fi
fi


if [[ $# -eq 2 || $# -eq 3 || $# -eq 4 ]]; then
	for file in `eval $with_obj`
	do
		file_basename=$(basename $file)
		if [[ $# -eq 2 ]]; then
			echo "\033[1;36m=>Command: $com_line $file\033[0m"
			eval $com_line $file
		elif [[ $# -eq 3 || $# -eq 4 ]]; then
			if [[ $mod_flag =~ '\+' ]]; then
				Command="$com_line $file ${pipe_out} ${redi_flag}${dir_output}${file_basename}${tag}"
				echo "\033[1;36m=>Command: $Command\033[0m"
				eval $Command
			elif [[ $mod_flag =~ '\-' ]]; then
				if [[ $file_basename =~ "^(.+)\.[^.]+$" ]]; then
					file_o_name=$match[1]
					Coammand="$com_line $file ${pipe_out} ${redi_flag}${dir_output}${file_o_name}"
					echo "\033[1;36m=>Command: $Command\033[0m"
					eval $Command
				fi
			elif [[ $mod_flag =~ '\=' ]]; then
				Command="$com_line $file ${pipe_out} ${redi_flag}${dir_output}${file_basename}"
				echo "\033[1;36m=>Command: $Command\033[0m"
				eval $Command
			elif [[ $mod_flag =~ '\#' ]]; then
				if [[ $file_basename =~ "^(.+)$tag_ori" ]]; then
					file_o_name=$match[1]
					Command="$com_line $file ${pipe_out} ${redi_flag}${dir_output}${file_o_name}${tag_mod}"
					echo "\033[1;36m=>Command: $Command\033[0m"
					eval $Command
				fi
			else
				echo "\033[0;31m**ERROR** incorrect mod flag! got \"$operations\", accept +, - or #!\033[0m"
			fi
		fi
	done
else
	echo "\033[0;31m**ERROR** incorrect arguments number! got $#, need 2 or 3!\033[0m"
fi
