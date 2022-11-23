from BigMartSales import logger
from BigMartSales.constants import * 
from BigMartSales.entity import DataValidationConfig
from BigMartSales.entity import DataIngestionArtifact, DataValidationArtifact
from BigMartSales.utils import read_yaml

import os,sys

# Eveidently is used for Data Drift etc 
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import numpy as np
import pandas as pd 
import json


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            logger.info(f"{'>>'*30} DataValidation started {'<<'*30} \n\n")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema = read_yaml(Path(self.data_validation_config.schema_file_path))
            self.current_time_stamp = CURRENT_TIME_STAMP

        except Exception as e:
            logger.exception(e)

    def get_train_test_dataset(self):
        try:

            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            return train_df,test_df 
        except Exception as e:
            logger.exception(e)

    def do_train_test_files_exist(self):
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

        
            is_file_exist = os.path.exists(train_file_path) and os.path.exists(test_file_path)

            logger.info(f"IS train and test File Exists? -> {is_file_exist}")


            return is_file_exist
        except Exception as e:
            logger.exception(e)
        
    def validation_dataset_schema(self) ->bool:
        try:
            validations_status = False

            schema_file = read_yaml(Path(self.data_validation_config.schema_file_path))
            schema_dict = schema_file[DATA_VALIDATION_SCHEMA_KEY]
            schema_domain_value = schema_file[SCHEMA_DOMAIN_VALUE_KEY]
            train_df , test_df = self.get_train_test_dataset()
            logger.info("Checking no. of columns in train and test dataset")
            if not len(schema_dict) == len(train_df.columns) and len(schema_dict) == len(test_df.columns):
                raise Exception("Train and/or test dataset does not have columns given in schema.")
            else:
                logger.info('No. of columns are same in train and test dataset and in schema file.')
                logger.info("Checking columns names")
                for column in schema_dict.keys():
                    if column not in train_df.columns:
                        raise Exception(f"Train dataset does not have column '{column}' mentioned in schema file")
                    if column not in test_df.columns:
                        raise Exception(f"Test dataset does not have column '{column}' mentioned in schema file")
                else:
                    logger.info(f"Train and test dataset have column required in schema file")
            logger.info("Checking the datatypes of all columns")
            for column in schema_dict.keys():
                if train_df[column].dtype == schema_dict[column] and test_df[column].dtype == schema_dict[column]:
                    logger.info(f"Column '{column}' has correct datatype in both train and test dataset.")
                else:
                    raise Exception(f"Column '{column}' does not have correct datatype in train and/or dataset.")

            logger.info("Checking the domain values of categorical columns")
            for column, cats in schema_domain_value.items():
                logger.info(f"Checking domain values of column '{column}'")
                for cat in train_df[column].unique():
                    if cat not in schema_domain_value[column]:
                        raise Exception(f"category '{cat}' is an unwanted value in column '{column}' of test dataset")
                for cat in test_df[column].unique():
                    if cat not in schema_domain_value[column]:
                        raise Exception(f"category '{cat}' is an unwanted value in column '{column}' of test dataset")
                else:
                    logger.info(f"column '{column}' has all the required categories and no extra category")
            logger.info("Data Validation Successful!")
            validations_status = True

            logger.info(f"Data Validation done and stats : {validations_status}")
            return validations_status
        except Exception as e:
            logger.exception(e)

    '''    def check_for_correlation(self):
        try:
            logger.info("Checking correlation between features")
            df,_  = self.get_train_test_dataset()
            target_column = self.schema[SCHEMA_TARGET_COLUMN_KEY][0]
            droppable_columns = []
            corr_matrix = df.corr(method='spearman',numeric_only=True)
            for column in df.columns:
                if np.abs(corr_matrix.loc[column,target_column]) < 0.1:
                    logger.info(f"Column [{column}] has very less correlation with the target feature.")
                    droppable_columns.append(column)
                    df.drop(column, axis=1, inplace=True)
            for i in corr_matrix.columns:
                for j in corr_matrix.columns:
                    if i!=j:
                        if corr_matrix.loc[i,j] > 0.7:
                            logger.info(f"Column [{i}[] and [{j}] has very high dependence on each other.")
                            df.drop(i, axis=1, inplace=True)
                            droppable_columns.append(column)
            logger.info(f"Droppable columns: {droppable_columns}")
            return droppable_columns
        except Exception as e:
            logger.exception(e)'''

    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])

            train_df ,test_df = self.get_train_test_dataset()
            test_df['Item_Outlet_Sales'] = 0 # 'Item_Outlet_Sales' not present in test so profile.calculate giving error 
            profile.calculate(train_df,test_df)

            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path

            report_dir = os.path.dirname(report_file_path)
            
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,'w') as report_file:
                json.dump(report,report_file,indent=6)
        
            return report

        except Exception as e:
            logger.exception(e)

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df ,test_df = self.get_train_test_dataset()
            test_df['Item_Outlet_Sales'] = 0 # 'Item_Outlet_Sales' not present in test so profile.calculate giving error 
            dashboard.calculate(train_df ,test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_paage_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_paage_dir,exist_ok=True)

            dashboard.save(report_page_file_path)
        except Exception as e:
            logger.exception(e)

    def is_data_drif_found(self) -> bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            logger.exception(e)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            self.do_train_test_files_exist()
            is_validated = self.validation_dataset_schema()
            self.is_data_drif_found()
            data_validation_artificat = DataValidationArtifact(
                                         schema_file_path=self.data_validation_config.schema_file_path,
                                         report_file_path=self.data_validation_config.report_file_path,
                                         report_page_file_path=self.data_validation_config.report_page_file_path,
                                         is_validated= is_validated,
                                         message=" data Validation Performed Successfully")

            logger.info(f'Data validation artifact : {data_validation_artificat}')

            return data_validation_artificat
        except Exception as e:
            logger.exception(e)
    def __del__(self):
        logger.info(f'{">>"*30} Data Validation completed {"<<"*30} \n\n')