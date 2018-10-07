#!/bin/sh
frequency=$1
filename="/sys/kernel/debug/clock/override.emc/rate"
echo $frequency > $filename
