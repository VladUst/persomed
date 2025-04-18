from src.services.diagnostic.ml_disease_prediction.get_prediction import get_prediction as ml_disease_prediction
from src.services.diagnostic.ontology_diseases_prediction.get_prediction import get_prediction as ontology_diseases_prediction
from src.services.diagnostic.ml_disease_prediction.get_prediction import get_model_info
from src.services.diagnostic.ontology_diseases_prediction.get_prediction import get_ontology_info

__all__ = [
    "ml_disease_prediction", 
    "ontology_diseases_prediction",
    "get_model_info",
    "get_ontology_info"
] 