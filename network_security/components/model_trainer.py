import os,sys
from network_security.exception.exception import NetworkSecuritySystem
from network_security.logging.logger import logging
import dagshub
dagshub.init(repo_owner='sheikhayanahmad710', repo_name='Network_Security', mlflow=True)



from network_security.entity.config_entity import DataTrainerConfig
from network_security.entity.artifact_entity import DataTransformationArtifact,DataTrainerArtifact

from network_security.utils.main_utils.utils import save_object,load_object,load_numpy_data,evaluate_models

from network_security.utils.ml_utils.model.estimator import Network_Model
from network_security.utils.ml_utils.metrics.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)
import mlflow


class ModelTrainer:
    def __init__(self,model_trainer_config:DataTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecuritySystem(e,sys)
        

    def track_mlflow(self,best_model,classification_train_metric):
        with mlflow.start_run():
            f1_score=classification_train_metric.f1_score
            precision_score=classification_train_metric.precision_score
            recall_score=classification_train_metric.recall_score

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(best_model,"model")
        
    def train_model(self,x_train,y_train,x_test,y_test):

        # ALL MODELS
        models = {
            "Random Forest":RandomForestClassifier(verbose=1),
            "Decision Tree":DecisionTreeClassifier(),
            "Ada Boost": AdaBoostClassifier(),
            "Logistic Regression": LogisticRegression(solver="saga", verbose=1),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
        }

        # PARAM GRIDS
        params = {
            "Random Forest": {
                "criterion": ["gini", "entropy"]
            },

            "Decision Tree": {
                "criterion": ["gini", "entropy"],
            },

            "Ada Boost": {
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.01, 0.1, 0.5, 1.0],
            },

            "Logistic Regression": {
                "C": [0.01, 0.1, 1, 10],
                "penalty": ["l1", "l2", "elasticnet"],
                "l1_ratio": [0.0, 0.5, 1.0]     # required for elasticnet
            },

            "Gradient Boosting": {
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.01, 0.1, 0.5],
            }
        }

        # CORRECT CALL
        model_report = evaluate_models(x_train, x_test, y_train, y_test, models, params)


        # BEST MODEL NAME
        best_model_score = max(model_report.values())
        best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

        logging.info(f"Best model name is {best_model_name}")

        best_model = models[best_model_name]

        # TRAIN METRICS
        y_train_pred = best_model.predict(x_train)
        classification_train_metric = get_classification_score(y_train_pred, y_train)


        #ML FLOW
        self.track_mlflow(best_model,classification_train_metric)

        # TEST METRICS
        y_test_pred = best_model.predict(x_test)
        classification_test_metric = get_classification_score(y_test_pred, y_test)

        self.track_mlflow(best_model,classification_test_metric)

        # Load preprocessor (correct key!)
        preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)

        os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_dir), exist_ok=True)

        network_model = Network_Model(preprocessor, best_model)

        # SAVE MODEL OBJECT (NOT CLASS!)
        save_object(self.model_trainer_config.trained_model_dir, network_model)

        save_object("final_model/model.pkl",best_model)

        # ARTIFACT
        model_trainer_artifact = DataTrainerArtifact(
            train_model_file_path=self.model_trainer_config.trained_model_dir,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric
        )

        logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")

        return model_trainer_artifact


    def initiate_model_trainer(self):
        try:
            # Load arrays
            train_arr = load_numpy_data(self.data_transformation_artifact.transoformed_train_file_path)
            test_arr  = load_numpy_data(self.data_transformation_artifact.transformed_test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            return self.train_model(x_train,y_train,x_test,y_test)

        except Exception as e:
            raise NetworkSecuritySystem(e,sys)
