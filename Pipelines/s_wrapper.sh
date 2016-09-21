STARTTIME=`python -c 'import time; print time.time()'`
echo "$*"
eval "$*"
echo "========================================================"
echo "run time: "$(bc -l <<< "scale=2; `python -c 'import time; print time.time()'`-$STARTTIME")s| tee -a $log
echo "========================================================"
doneRemind "work done!"