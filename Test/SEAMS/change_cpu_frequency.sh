#!/bin/sh
frequency=$1
cpu_name=$2
max_file="/sys/devices/system/cpu/$cpu_name/cpufreq/scaling_max_freq"
min_file="/sys/devices/system/cpu/$cpu_name/cpufreq/scaling_min_freq"
governor_file="/sys/devices/system/cpu/$cpu_name/cpufreq/scaling_governor"
echo userspace > $governor_file
echo $frequency > $max_file
echo $frequency > $min_file
