#!/usr/bin/python
import os 
import sys
import commands 
import subprocess
import itertools 
from ConfigParams import ConfigParams
from params_file import params

class GenerateParams(object):
    """This class is used to generate parameters for running inference
    """
    def __init__(self,logger):
        self.logger=logger
        self.logger.info("Initializing GenerateParams Class")
        
        # get big core frequencies 
        self.big_core_freqs=self.get_big_core_freqs()
        self.big_core_freqs = filter(None, self.big_core_freqs)
        
        self.big_cores=["cpu0",
                        "cpu1",
                        "cpu2",
                        "cpu3"]
        self.ENABLE="1"
        self.DISABLE="0"
        
        # get gpu frequencies
        self.gpu_freqs=self.get_gpu_freqs()
        self.gpu_freqs=self.freq_conversion(self.gpu_freqs)
        
        # get emmc frequencies
        self.emmc_freqs=self.get_emmc_freqs()
        self.emmc_freqs=self.freq_conversion(self.emmc_freqs)
        
        # generate all possible combinations 
        #self.generate_params_combination()
        #self.get_valid_params()
        self.params=params    
        # set config 
        for conf in self.params:
             ConfigParams(logger,conf)
           
    def freq_conversion(self,array):
        """This function is is used to convert frequency from KHz to Hz
        """
        array.pop()
        array=[i+"000" for i in array]
        return array

    def get_big_core_freqs(self):
        """This function is used to get available frequencies for all the big cores
        @returns:
            freq: list of available frequencies for big cores
        """
        try:
            freq=commands.getstatusoutput("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies")[1]
            if freq:
                freq=freq.split(" ")
                return freq
        except:
            self.logger.error ("big core frequency file does not exist")

    def get_gpu_freqs(self):
        """This function is used to get available gpu frequencies
        @returns:
            freq: list of available frequencies for gpus
        """
        try:
            freq=commands.getstatusoutput("cat /sys/kernel/debug/clock/gbus/possible_rates")[1]
            if freq:
                freq=freq.split(" ")
                return freq
        except:
            self.logger.error ("gbus frequency file does not exist")

    def get_emmc_freqs(self):
        """This function is used to get available emmc frequencies
        @returns:
            freq: list of available frequencies for emmc controller
        """
        try:
            freq=commands.getstatusoutput("cat /sys/kernel/debug/clock/emc/possible_rates")[1]
            if freq:
                freq=freq.split(" ")
                return freq
        except:
            self.logger.error ("emmc frequency file does not exist")
    
    def generate_params_combination(self):
        """This function is used to generate parameter combinations 
        """
        # core status
        cpu0_status=[self.ENABLE]
        cpu1_status=[self.ENABLE,self.DISABLE]
        cpu2_status=[self.ENABLE,self.DISABLE]
        cpu3_status=[self.ENABLE,self.DISABLE]
        
        # core frequency
        cpu0_freqs=self.big_core_freqs
        cpu1_freqs=self.big_core_freqs
        cpu2_freqs=self.big_core_freqs
        cpu3_freqs=self.big_core_freqs
        
        # gpu status
        gpu_status=[self.ENABLE,self.DISABLE]
        
        # emmc status 
        emmc_status=[self.ENABLE,self.DISABLE]
        # master data
        max_gpu_freq=[self.gpu_freqs[-1]]   
        
        var=[cpu0_status,   #0
             cpu0_freqs,    #1
             cpu1_status,   #2
             cpu1_freqs,    #3
             cpu2_status,   #4
             cpu2_freqs,    #5
             cpu3_status,   #6
             cpu3_freqs,    #7
             gpu_status,    #8
             max_gpu_freq   #9
             ]
        
        self.params=list(itertools.product(*var))
        
    def get_valid_params(self):
        """This function is used to extract the valid params from all the combination of params
        """
        # set frequency values to null when cou/gpu/emmc is disabled
        for i in range(len(self.params)):
            self.params[i]=list(self.params[i])
            for j in range(0,len(self.params[i]),2):
                if self.params[i][j]==self.DISABLE:
                    self.params[i][j+1]=None

        # remove duplicates
        self.params.sort()
        self.params=list(self.params for self.params,_ in itertools.groupby(self.params))
        # save to a file for temporary use 
        with open('params_file.py', 'w') as f:
            f.write('params = %s' %self.params)
       
                              
