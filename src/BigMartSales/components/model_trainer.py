import sys
from pathlib import Path
from BigMartSales import logger
from BigMartSales.entity import DataTransformationArtifact, ModelTrainerArtifact
from BigMartSales.entity import ModelTrainerConfig
from BigMartSales.utils import load_numpy_array_data,save_object,load_object
from BigMartSales.entity import MetricInfoArtifact,evaluate_regression_model,ModelFactory,GridSearchedBestModel
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score,mean_absolute_error
import numpy as np
from typing import List


class salesEstimatorModel:
    def __init__(self, preprocessing_object, trained_model_object):
        """
        preprocessing_object: preprocessing_object
        trained_model_object: trained_model_object
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, X):
        """
        function accepts raw inputs and then transformed raw input using preprocessing_object
        which gurantees that the inputs are in the same format as the training data
        At last it perform prediction on transformed features
        """
        transformed_feature = self.preprocessing_object.transform(X)
        return self.trained_model_object.predict(transformed_feature)

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"




class ModelTrainer:

    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            logger.info(f"{'>>' * 30}Model trainer log started.{'<<' * 30} ")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            logger.exception(e)

    '''def get_best_param_rf(self,x_train,y_train,x_test,y_test):
        try:
            best_params={}

            param1={'criterion': ['squared_error', 'absolute_error']}
            param2={'max_depth' : range(3,10,1)}
            param3={'max_features' : [i/100.0 for i in range(70,100,3)]}
            param4={'max_samples' : [i/100.0 for i in range(70,100,5)]}
            param5={'n_estimators':range(10,100,5)}


            parameters=[param1, param2, param3, param4, param5]

            for param in parameters:
                grid =GridSearchCV(RandomForestRegressor(), param, cv=5, n_jobs=-1)
                grid.fit(x_train, y_train)
                best_params.update(grid.best_params_)

            criterion=best_params['criterion']
            max_depth=best_params['max_depth']
            max_features=best_params['max_features']
            max_samples=best_params['max_samples']
            n_estimators=best_params['n_estimators']



            model=RandomForestRegressor(criterion=criterion, max_depth = max_depth, max_features = max_features, max_samples = max_samples, n_estimators = n_estimators)
            model.fit(x_train, y_train)
            y_pred=model.predict(x_test)

            r2=r2_score(y_test, y_pred)
            return model, r2
        except Exception as e:
            logger.exception(e)'''

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            logger.info(f"Loading transformed training dataset")
            transformed_train_file_path = Path(self.data_transformation_artifact.transformed_train_file_path)
            train_array = load_numpy_array_data(file_path=transformed_train_file_path)

            logger.info(f"Loading transformed testing dataset")
            transformed_test_file_path = Path(self.data_transformation_artifact.transformed_test_file_path)
            test_array = load_numpy_array_data(file_path=transformed_test_file_path)

            logger.info(f"Splitting training and testing input and target feature")
            x_train,y_train,x_test,y_test = train_array[:,:-1],train_array[:,-1],test_array[:,:-1],test_array[:,-1]
         
            logger.info(f"Extracting model config file path")
            model_config_file_path = Path(self.model_trainer_config.model_config_file_path)
            logger.info(f"Initializing model factory class using above model config file: {model_config_file_path}")
            model_factory = ModelFactory(model_config_path=model_config_file_path)
            base_accuracy = self.model_trainer_config.base_accuracy
            logger.info(f"Expected accuracy: {base_accuracy}")
            logger.info(f"Initiating operation model selection")
            best_model = model_factory.get_best_model(X=x_train,y=y_train,base_accuracy=base_accuracy)
            logger.info(f"Extracting trained model list.")
            grid_searched_best_model_list:List[GridSearchedBestModel]=model_factory.grid_searched_best_model_list
            model_list = [model.best_model for model in grid_searched_best_model_list]
            logger.info(f"Evaluating all trained model on training and testing dataset both")

            metric_info:MetricInfoArtifact = evaluate_regression_model(model_list=[best_model],X_train=x_train,
                                                                        y_train=y_train,X_test=x_test,
                                                                        y_test=y_test,base_accuracy=base_accuracy)
            logger.info(f"Best found model on both training and testing dataset.")
            preprocessing_obj=  load_object(file_path=Path(self.data_transformation_artifact.preprocessed_object_file_path))
            model_object = metric_info.model_object 
            trained_model_file_path=Path(self.model_trainer_config.trained_model_file_path)

            data_model = salesEstimatorModel(preprocessing_object=preprocessing_obj,trained_model_object=model_object)
            logger.info(f"Saving model at path: {trained_model_file_path}")
            save_object(file_path=trained_model_file_path,obj=data_model)
            
            model_trainer_artifact= ModelTrainerArtifact(is_trained=True,message="Model Trained successfully",
                                    trained_model_file_path=trained_model_file_path,
                                    train_rmse=metric_info.train_rmse,
                                    test_rmse=metric_info.test_rmse,
                                    train_accuracy=metric_info.train_accuracy,
                                    test_accuracy=metric_info.test_accuracy,
                                    model_accuracy=metric_info.model_accuracy)
            logger.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            logger.exception(e)

    def __del__(self):
        logger.info(f"{'>>' * 30}Model trainer log completed.{'<<' * 30} ") 