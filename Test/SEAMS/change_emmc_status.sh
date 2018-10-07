#!/bin/sh
status=$1
filename="/sys/kernel/debug/clock/override.emc/state"
echo $status > $filename

