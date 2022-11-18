
from BigMartSales import logger
import os,sys
from BigMartSales.constants import *
from BigMartSales.entity import DataIngestionConfig
from BigMartSales.entity import DataIngestionArtifact
import requests
import zipfile
import shutil
import pandas as pd 

from sklearn.model_selection import train_test_split



class DataIngestion:
    def __init__(self,data_ingestion_config=DataIngestionConfig):
        try:
            logger.info(f'{">"*30} Data Ingestion Started {"<"*30}')
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            logger.exception(e)


    def download_data(self)->str:
        try:

            download_url = self.data_ingestion_config.dataset_download_url

            zip_download_dir = self.data_ingestion_config.zip_download_dir
            
            logger.info(f"Downloading file from : {download_url} into : {zip_download_dir} ")
            
            os.makedirs(zip_download_dir,exist_ok=True)
            os.chdir(zip_download_dir)
            
            r  = requests.get(download_url)
        
            with open('data.zip','wb') as f:
                f.write(r.content)

            logger.info(f"File downloaded successfully  {zip_download_dir} ")

            return zip_download_dir
        except Exception as e:
            logger.exception(e)


    def extract_data(self,zip_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)

            logger.info(f"Extracting zip file {zip_file_path} into dir {raw_data_dir} ")

            
            os.chdir(zip_file_path)
            with zipfile.ZipFile('data.zip','r') as data_zip:
                os.chdir(raw_data_dir)
                print(data_zip.extractall())
                os.remove('test.csv')
                os.rename('Train.csv','data.csv')

            logger.info(f'{">"*20} Extraction completed {"<"*20}')

        except Exception as e:
            logger.exception(e)


    def split_data_as_train_test(self) ->DataIngestionArtifact:
        try :
            
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            data_file_path = os.path.join(raw_data_dir,file_name)

            logger.info(f"Reading csv file: [{data_file_path}]")
            data_frame = pd.read_csv(data_file_path)

            logger.info(f"Splitting data into train and test with test data ration = 0.2")

            train, test = train_test_split(data_frame,test_size=0.2,random_state=42)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        file_name)

            os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
            logger.info(f"Exporting training datset to file: [{train_file_path}]")
            train.to_csv(train_file_path,index=False)                            

            os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
            logger.info(f"Exporting test dataset to file: [{test_file_path}]")
            test.to_csv(test_file_path,index=False)
            
            is_ingested = True

            message = f"Data ingestion completed successfully."

            data_ingestion_artifact = DataIngestionArtifact(
                                        train_file_path=train_file_path,
                                        test_file_path=test_file_path,
                                        is_ingested=is_ingested,
                                        message=message
            )

            logger.info(f'data_ingestion_artifact : [{data_ingestion_artifact}]')
            return data_ingestion_artifact

        except Exception as e:
            logger.exception(e)


    
    def initiate_data_ingestion(self) ->DataIngestionArtifact:
        try:
            zip_file_path = self.download_data()

            self.extract_data(zip_file_path=zip_file_path)

            return self.split_data_as_train_test()
        except Exception as e:
            logger.exception(e)


    def __del__(self):
        
        logger.info(f'{">"*40} Data Ingestion completed {"<"*40} \n\n')