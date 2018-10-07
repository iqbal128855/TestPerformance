import logging
import socket
import os
import sys
from datetime import datetime
from src.GenerateParams import GenerateParams

def config_logger():
    """This function is used to configure logging information
    @returns logger logging object
    """
    log_dir=os.getcwd()
    d=datetime.now()
    log_file_name="logfile_"+str(d.date())
    log_file=os.path.join(log_dir,log_file_name)

    ip=socket.gethostbyname(socket.gethostname())
    extra={"ip_address":ip}
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger=logging.getLogger(__name__)
    hdlr = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(ip_address)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    logger = logging.LoggerAdapter(logger, extra)
    logger.info("Start RunTest")
    return logger

if __name__=="__main__":
    logger=config_logger()
    GP=GenerateParams(logger)
