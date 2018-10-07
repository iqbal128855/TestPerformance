#!/bin/sh
status=$1
filename="/sys/kernel/debug/clock/override.gbus/state"
echo $status > $filename

