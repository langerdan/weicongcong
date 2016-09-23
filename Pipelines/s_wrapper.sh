#!/bin/zsh
# -*- coding: utf-8 -*-
# PROGRAM : s_wrapper
# AUTHOR  : codeunsolved@gmail.com
# CREATED : September 21 2016
# VERSION : v0.0.1a

echo "========================================================"
echo "\033[1;32m$(date)\033[0m"
echo "========================================================"
STARTTIME=`python -c 'import time; print time.time()'`
Command=""
for x in "$@"
do
	if [[ $x =~ ' ' ]]; then
		x=\"$x\"
	fi
	Command="$Command $x"
done
echo "\033[1;36mCommand: $Command\033[0m"
echo "========================================================"
eval $Command
echo "========================================================"
echo "\033[1;32mrun time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$STARTTIME")"s\033[0m"
echo "========================================================"
doneRemind "mission complete!"