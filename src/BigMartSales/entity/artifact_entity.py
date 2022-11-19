from collections import namedtuple


DataIngestionArtifact = namedtuple("DataIngestionArtifact",["train_file_path",
                                    "test_file_path","is_ingested","message"])

DataValidationArtifact = namedtuple("DataIngestionArtifac",["schema_file_path",'report_file_path','report_page_file_path','is_validated','message'])

DataTransformationArtifact = namedtuple("DataTransformationArtifact",
 ["is_transformed", "message", "transformed_train_file_path","transformed_test_file_path",
     "preprocessed_object_file_path","transformed_train_arr_df_sorce","transformed_test_arr_df_source"])