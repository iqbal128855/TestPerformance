#!/bin/sh
frequency=$1
filename="/sys/kernel/debug/clock/override.gbus/rate"
echo $frequency > $filename
