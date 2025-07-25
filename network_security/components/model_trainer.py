import os
import sys
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import (
    DataTransformationConfig,
    ModelTrainerConfig,
)
from network_security.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
)
from network_security.utils.ml_utils.model.estimator import NetworkModel
from network_security.utils.ml_utils.metric.classification_metric import (
    get_classification_score,
)
from network_security.utils.main_utils.utils import (
    evaluate_models,
    save_object,
    load_object,
    load_numpy_array_data,
)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier,
)
import mlflow
import mlflow.sklearn
import dagshub
from dotenv import load_dotenv

load_dotenv()

DAGSHUB_REPO_OWNER = os.getenv("DAGSHUB_REPO_OWNER")
DAGSHUB_REPO_NAME = os.getenv("DAGSHUB_REPO_NAME")

dagshub.init(repo_owner=DAGSHUB_REPO_OWNER, repo_name=DAGSHUB_REPO_NAME, mlflow=True)


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact,
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def track_mlflow(self, best_model, classification_metric):
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            precision_score = classification_metric.precision_score
            recall_score = classification_metric.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision", precision_score)
            mlflow.log_metric("recall_score", recall_score)
            mlflow.sklearn.log_model(sk_model=best_model, artifact_path="model")

    def train_model(self, X_train, y_train, x_test, y_test) -> ModelTrainerArtifact:
        models = {
            "RandomForestClassifier": RandomForestClassifier(verbose=1),
            "DecisionTreeClassifier": DecisionTreeClassifier(),
            "GradientBoostingClassifier": GradientBoostingClassifier(verbose=1),
            "LogisticRegression": LogisticRegression(verbose=1),
            "AbaBoostClassifier": AdaBoostClassifier(),
        }

        params = {
            "RandomForestClassifier": {
                "criterion": ["gini", "entropy", "log_loss"],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "DecisionTreeClassifier": {
                # 'criterion':['gini', 'entropy', 'log_loss'],
                # 'max_features':['sqrt','log2',None],
            },
            "GradientBoostingClassifier": {
                # 'loss':['log_loss', 'exponential'],
                "learning_rate": [0.1, 0.01, 0.05, 0.001],
                "subsample": [0.6, 0.7, 0.75, 0.85, 0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                "n_estimators": [8, 16, 32, 64, 128, 256],
            },
            "LogisticRegression": {},
            "AbaBoostClassifier": {
                "learning_rate": [0.1, 0.01, 0.001],
                "n_estimators": [8, 16, 32, 64, 128, 256],
            },
        }

        model_report: dict = evaluate_models(
            X_train=X_train,
            y_train=y_train,
            X_test=x_test,
            y_test=y_test,
            param=params,
            models=models,
        )

        ## Get best model score from dict
        best_model_score = max(sorted(model_report.values()))

        ## Get best model name from dict
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]

        best_model = models[best_model_name]

        y_train_pred = best_model.predict(X_train)

        classification_train_metric = get_classification_score(
            y_true=y_train, y_pred=y_train_pred
        )

        self.track_mlflow(best_model, classification_train_metric)

        y_test_pred = best_model.predict(x_test)
        classification_test_metric = get_classification_score(
            y_true=y_test, y_pred=y_test_pred
        )

        self.track_mlflow(best_model, classification_test_metric)

        preprocessor = load_object(
            file_path=self.data_transformation_artifact.transformed_object_file_path
        )

        model_dir_path = os.path.dirname(
            self.model_trainer_config.trained_model_file_path
        )
        os.makedirs(model_dir_path, exist_ok=True)

        network_model = NetworkModel(
            model=best_model,
            preprocessor=preprocessor,
        )

        save_object(
            file_path=self.model_trainer_config.trained_model_file_path,
            obj=network_model,
        )

        ## Save best model to final model path
        save_object("final_model/model.pkl", obj=best_model)

        ## Model Trainer Artifact
        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric,
        )

        logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
        return model_trainer_artifact

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = (
                self.data_transformation_artifact.transformed_train_file_path
            )
            test_file_path = (
                self.data_transformation_artifact.transformed_test_file_path
            )

            ## load training and testing array
            train_array = load_numpy_array_data(file_path=train_file_path)
            test_array = load_numpy_array_data(file_path=test_file_path)

            ## split training and testing array into features and target
            X_train, y_train = train_array[:, :-1], train_array[:, -1]
            x_test, y_test = test_array[:, :-1], test_array[:, -1]

            model_trainer_artifact = self.train_model(
                X_train=X_train, y_train=y_train, x_test=x_test, y_test=y_test
            )
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
