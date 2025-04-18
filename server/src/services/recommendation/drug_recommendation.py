from owlready2 import *
import os
from datetime import datetime


def get_drug_recommendations(disease_name):
    """
    Get drug recommendations for a specific disease from the ontology.
    
    Args:
        disease_name (str): The name of the disease to find recommendations for
        
    Returns:
        list: List of drug names recommended for the disease
    """
    # Load the ontology
    pre = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(pre))
    onto_path = os.path.join(parent_dir, "services/ontology/diseases.owl")
    onto = get_ontology(onto_path).load()
    
    # SPARQL запрос для поиска препаратов, которые используются для лечения заболевания
    # Используется отношение treated_with от заболевания к препарату
    # Запрос не чувствителен к регистру благодаря FILTER(LCASE(?disease_name) = LCASE("..."))
    drug_query = f"""
    PREFIX dis: <http://www.semanticweb.org/dorsa/ontologies/diseases.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT DISTINCT ?drug_name
    WHERE {{
        ?disease rdf:type dis:disease .
        ?disease dis:full_name ?disease_name .
        FILTER(LCASE(?disease_name) = LCASE("{disease_name}"))
        ?disease dis:treated_with ?drug .
        ?drug dis:full_name ?drug_name .
    }}
    """
    
    # Execute the query
    drugs = list(default_world.sparql(drug_query))
    
    # Extract drug names from query results
    drug_names = [drug[0] for drug in drugs] if drugs else []
    
    # Если препараты не найдены, попробуем найти с использованием отношения treats (обратное к treated_with)
    if not drug_names:
        drug_query_alt = f"""
        PREFIX dis: <http://www.semanticweb.org/dorsa/ontologies/diseases.owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT DISTINCT ?drug_name
        WHERE {{
            ?disease rdf:type dis:disease .
            ?disease dis:full_name ?disease_name .
            FILTER(LCASE(?disease_name) = LCASE("{disease_name}"))
            ?drug dis:treats ?disease .
            ?drug dis:full_name ?drug_name .
        }}
        """
        drugs_alt = list(default_world.sparql(drug_query_alt))
        drug_names = [drug[0] for drug in drugs_alt] if drugs_alt else []
    
    return drug_names


def get_ontology_info():
    """
    Get information about the ontology's drugs and diseases.
    
    Returns:
        str: Information about the number of drugs and diseases in the ontology
    """
    # Load the ontology
    pre = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(pre))
    onto_path = os.path.join(parent_dir, "services/ontology/diseases.owl")
    onto = get_ontology(onto_path).load()
    
    # Query for diseases
    diseases_query = """
    PREFIX dis: <http://www.semanticweb.org/dorsa/ontologies/diseases.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT DISTINCT ?d
    WHERE {?d rdf:type dis:disease .}
    """
    diseases = list(default_world.sparql(diseases_query))
    disease_count = len(diseases)
    
    # Query for drugs
    drugs_query = """
    PREFIX dis: <http://www.semanticweb.org/dorsa/ontologies/diseases.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT DISTINCT ?d
    WHERE {?d rdf:type dis:drug .}
    """
    drugs = list(default_world.sparql(drugs_query))
    drug_count = len(drugs)
    
    return f"Онтология заболеваний и препаратов. Онтология связывает {disease_count} заболеваний и {drug_count} лекарственных препаратов"


def get_current_date():
    """
    Get the current date formatted as a string.
    
    Returns:
        str: Current date in the format DD.MM.YYYY
    """
    now = datetime.now()
    return now.strftime("%d.%m.%Y")
