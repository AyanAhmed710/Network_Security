from network_security.entity.artifact_entity import ClassificationmeticArtifact
from sklearn.metrics import f1_score,recall_score,precision_score
from network_security.exception.exception import NetworkSecuritySystem
import sys

def get_classification_score(y_pred,y_true):
    try:

     model_f1_score=f1_score(y_true,y_pred)
     model_recall_score=recall_score(y_true,y_pred)
     model_precision_score=precision_score(y_true,y_pred)

     classification_metric=ClassificationmeticArtifact(
        f1_score=model_f1_score,
        recall_score=model_recall_score,
        precision_score=model_precision_score
        

    )

     return classification_metric
    
    except Exception as e:
       raise NetworkSecuritySystem(e,sys)

