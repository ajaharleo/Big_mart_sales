import os,sys
import logging
from BigMartSales.constants import *
import pandas as pd


logging_str = '[%(asctime)s]^;%(levelname)s^;%(lineno)d^;%(filename)s^;%(funcName)s()^;%(message)s'
log_dir = "logs"
log_filepath = os.path.join(log_dir, f"log_{get_current_time_stamp()}.log")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO, 
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ])

logger = logging.getLogger("BigMartLogger")

def get_log_dataframe(file_path:Path):
    data=[]
    if os.path.getsize(file_path):
        with open(file_path) as log_file:
            for line in log_file.readlines():
                data.append(line.split("^;"))

        log_df = pd.DataFrame(data)
        columns=["Time stamp","Log Level","line number","file name","function name","message"]
        log_df.columns=columns
        
        log_df["log_message"] = log_df['file name'].astype(str)+'>>>>>Line no:'+log_df['line number'].astype(str)+'>>>>>'+log_df['Time stamp'].astype(str) +":$"+ log_df["message"]
        return log_df[["log_message"]]
    else:
        return pd.DataFrame(['NO DATA IN THE LOG FILE!!!! PLEASE CHECK ANOTHER FILE.'])