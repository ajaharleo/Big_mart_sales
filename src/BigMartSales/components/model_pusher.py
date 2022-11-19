from BigMartSales import logger
from BigMartSales.entity import ModelPusherArtifact, ModelEvaluationArtifact 
from BigMartSales.entity import ModelPusherConfig
import os, sys
import shutil


class ModelPusher:

    def __init__(self, model_pusher_config: ModelPusherConfig,
                 model_evaluation_artifact: ModelEvaluationArtifact
                 ):
        try:
            logger.info(f"{'>>' * 30}Model Pusher log started.{'<<' * 30} ")
            self.model_pusher_config = model_pusher_config
            self.model_evaluation_artifact = model_evaluation_artifact

        except Exception as e:
            logger.exception(e)

    def export_model(self) -> ModelPusherArtifact:
        try:
            evaluated_model_file_path = self.model_evaluation_artifact.evaluated_model_path
            export_dir = self.model_pusher_config.export_dir_path
            model_file_name = os.path.basename(evaluated_model_file_path)
            export_model_file_path = os.path.join(export_dir, model_file_name)
            logger.info(f"Exporting model file: [{export_model_file_path}]")
            os.makedirs(export_dir, exist_ok=True)

            shutil.copy(src=evaluated_model_file_path, dst=export_model_file_path)
            #we can call a function to save model to Azure blob storage/ google cloud strorage / s3 bucket
            logger.info(
                f"Trained model: {evaluated_model_file_path} is copied in export dir:[{export_model_file_path}]")

            model_pusher_artifact = ModelPusherArtifact(is_model_pusher=True,
                                                        export_model_file_path=export_model_file_path
                                                        )
            logger.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            return model_pusher_artifact
        except Exception as e:
            logger.exception(e)

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            return self.export_model()
        except Exception as e:
            logger.exception(e)

    def __del__(self):
        logger.info(f"{'>>' * 20}Model Pusher log completed.{'<<' * 20} ")