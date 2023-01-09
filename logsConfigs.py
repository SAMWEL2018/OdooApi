from datetime import datetime
from configs import Configs
import  logging
cfg = Configs()
import os

def log(level,msg):
    date = datetime.now().strftime("%Y%m%d")

    if not os.path.isdir(cfg.logd):
        os.makedirs(cfg.logd)

    logging.basicConfig(filemode='a',filename=cfg.logd+str(date)+'.log',
                        format=('%(asctime)s - %(levelname)s - %(message)s'))
    logs =  logging.getLogger()
    logs.setLevel(logging.DEBUG)
    logs.addHandler(logging.StreamHandler())

    if(level==1):
        logs.info(msg)
    elif(level==2):
        logs.error(msg)
    elif(level==3):
        logs.warning(msg)
    elif(level==4):
        logs.debug(msg)
    else:
        print("Unknown error")




