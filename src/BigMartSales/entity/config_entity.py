from collections import namedtuple

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])

DataIngestionConfig = namedtuple("DataIngestionConfig",
                    ['dataset_download_url','zip_download_dir','raw_data_dir',
                    'ingested_train_dir','ingested_test_dir','ingested_dir'])

DataValidationConfig = namedtuple("DataValidationConfig",['schema_file_path','report_file_path','report_page_file_path'])

DataTransformationConfig = namedtuple("DataTransformationConfig", ["transformed_train_dir",
                                                                   "transformed_test_dir",
                                                                   "preprocessed_object_file_path",
                                                                   "transformed_train_file",
                                                                   "transformed_test_file"
                                                                   ])