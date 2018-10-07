#!/usr/bin/python
import os 
import sys
import commands
import subprocess

class ConfigParams(object):
    """This class is used to create different confiuration space for jetson  tx1
    """
    def __init__(self,logger,cur_config):
        print ("Initializing ConfigParams Class")
        self.logger=logger
        self.cur_config=cur_config
        self.logger.info ("----------Current Config: " + str(self.cur_config)+ "----------")
        # define constant variables
        self.CPU0=0
        self.CPU1=2
        self.CPU2=4
        self.CPU3=6
        self.GPU=8
        self.EMMC=10
        self.ENABLE="1"
        self.DISABLE="0"
        # set specific configuration
        for index in range(0,len(self.cur_config),2):
            status=self.cur_config[index]
            freq=self.cur_config[index+1]

            # cpu0
            if index==self.CPU0:
                if status==self.ENABLE:
                    self.set_big_core_freqs("cpu0",freq)
                else:
                    self.logger.error("invalid status for cpu0")
            #cpu1
            if index==self.CPU1:
                self.set_big_core_status("cpu1",status)
                self.set_big_core_freqs("cpu1",freq)
            #cpu2
            if index==self.CPU2:
                self.set_big_core_status("cpu2",status)
                self.set_big_core_freqs("cpu2",freq)
            #cpu3
            if index==self.CPU3:
                self.set_big_core_status("cpu3",status)
                self.set_big_core_freqs("cpu3",freq)
            #gpu 
            if index==self.GPU:
                self.set_gpu_status(status)
                self.set_gpu_freqs(freq)
            #emmc
            if index==self.EMMC:
                self.set_emmc_status(status)
                self.set_emmc_freqs(freq)
            
          
    def set_big_core_status(self,cpu_name,status):
        """This function is used set core status (enable or disable)
        @input:
             cpu_name: cpu that will be enabled or disabled
        @returns:
        boolean: whether the operation was successful or not  
        """
        #print("cpu status")
        if cpu_name!="cpu0":
            cur_status=commands.getstatusoutput("cat /sys/devices/system/cpu/"+cpu_name+"/online")[1]   
            if cur_status!=status:
                subprocess.call(["sudo","sh","./change_core_status.sh",str(cpu_name),str(status)])
                # check if the operation is successful
                new_status= commands.getstatusoutput("cat /sys/devices/system/cpu/"+cpu_name+"/online")[1]
                if new_status!=status:
                    self.logger.error("cpu status did not change for "+ str(cpu_name))
        else:
            self.logger.error("invalid cpu_name argument")

    def set_big_core_freqs(self,cpu_name,frequency):
        """This function is used to set core frequency of one or more cores
        @input:
            frequency- clockspeed at what the cpu will be set 
            cpu_name- cpu number which will be set
        @returns:
            boolean- whether the set operation was successful or not   
        """
        #print ("cpu frequency")
        if frequency is not None:
            subprocess.call(["sudo","sh","./change_cpu_frequency.sh",str(frequency),str(cpu_name)])
            new_freq=commands.getstatusoutput("cat /sys/devices/system/cpu/"+cpu_name+"/cpufreq/scaling_cur_freq")[1]
            if str(new_freq)!=str(frequency):
                self.logger.error ("frequency of "+ str(frequency)+ " for  "+ str(cpu_name) + " did not change" )
            return True  
       
    def set_gpu_status(self,status):
        """This function is used to change gpu status
        @input:
            status: the status for gpu 
        """
        #print ("gpu status")
        cur_status=commands.getstatusoutput("cat /sys/kernel/debug/clock/gbus/state")[1]
        if cur_status!=status:
            subprocess.call(["sudo","sh","./change_gpu_status.sh",str(status)])
            # check if the operation is successful 
            new_status=commands.getstatusoutput("cat /sys/kernel/debug/clock/gbus/state")[1]
            if new_status!=status:
                self.logger.error("gpu status did not change")
            return True
        

    def set_gpu_freqs(self,frequency):
        """This function is used to change gpu clockspeeds
        @input:
           frequency: the clockspeed at which the gpu will be set
        """
        #print("gpu frequency")
        if frequency is not None:
            subprocess.call(["sudo","sh","./change_gpu_frequency.sh",str(frequency)])
            # check if the operation is successful 
            new_freq=commands.getstatusoutput("cat /sys/kernel/debug/clock/gbus/rate")[1]
            if new_freq!=frequency:
                self.logger.error ("gpu frequency "+ str(frequency) + " did not change")
        return True
    
    def set_emmc_status(self,status):
        """This function is used to change emmc status
        @input:
            status: the status for emmc 
        """
        #print ("emc status")
        cur_status=commands.getstatusoutput("cat /sys/kernel/debug/clock/emc/state")[1]
        if cur_status!=status:
            subprocess.call(["sudo","sh","./change_emmc_status.sh",str(status)])
            # check if the operation is successful 
            new_status=commands.getstatusoutput("cat /sys/kernel/debug/clock/emc/state")[1]
            if new_status!=status:
                self.logger.error("emc status did not change")    
            return True        

    def set_emmc_freqs(self,frequency):
        """This function is used to change emmc clockspeeds
        @input:
        frequency: the clockspeed at which the emmc will be set
        """
        #print ("emc frequency")
        if frequency is not None:
            subprocess.call(["sudo","sh","./change_emmc_frequency.sh",str(frequency)])
            # check if the operation is successful 
            new_freq=commands.getstatusoutput("cat /sys/kernel/debug/clock/emc/rate")[1]
        
            if new_freq!=frequency:
                self.logger.error ("emc frequency "+ str(frequency) + " did not change")

            return True

