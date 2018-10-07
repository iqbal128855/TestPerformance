#!/usr/bin/python
import os 
import sys
import commands
from multiprocessing import Process
from apscheduler.schedulers.background import BackgroundScheduler
class ComputePerformance(object):
    """This function is used to compute cpu,gpu and total power and measure inference time
    """
    def __init__(self):
        print ("Initializing Compute Performance Class")
        #self.logger=logger
        #self.cur_config=cur_config
        self.total_power=[]
        self.sched=BackgroundScheduler()
        self.sched.add_job(self.compute_power,"interval",seconds=.001)
        self.sched.start()
        self.compute_inference_time()
        self.sched.shutdown()
        print (self.total_power)
    
    def compute_power(self):
        """This function is used to compute power 
        """
        [total_power,
        gpu_power,
        cpu_power]=[None,None,None]
        try:
            self.total_power.append(commands.getstatusoutput("cat /sys/devices/platform/7000c400.i2c/i2c-1/1-0040/iio_device/in_power0_input")[1])
            
        except:    #TODO
            self.logger.error("error in power measurement")
     
    def compute_inference_time(self):
        """This function is used to compute inference time
        """
        for i in range(0,10000):
            print ("compute inference time")

if __name__=="__main__":
    CP=ComputePerformance()
