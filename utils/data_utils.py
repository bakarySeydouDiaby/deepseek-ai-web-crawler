import csv

from models.cours_javascript import coursDeJavascript


def is_duplicate_cours(nom_cours: str, noms_vus: set) -> bool:
    """
    Vérifie si une cours de javascript est un doublon.
    
    Args:
        nom_cours: Nom du cours à vérifier
        noms_vus: Ensemble des noms déjà vus
        
    Returns:
        bool: True si la cours est un doublon, False sinon
    """
    return nom_cours in noms_vus


def is_complete_cours(cours: dict, required_keys: list) -> bool:
    """
    Vérifie si un cours de javascript contient toutes les informations requises.
    
    Args:
        cours: Dictionnaire contenant les informations de la cours
        required_keys: Liste des clés requises
        
    Returns:
        bool: True si la cours est complète, False sinon
    """
    return all(key in cours for key in required_keys)


def save_cours_javascript_to_csv(cours: list, filename: str):
    """
    Sauvegarde la liste des cours de javascript dans un fichier CSV.
    
    Args:
        cours: Liste des cours de javascript à sauvegarder
        filename: Nom du fichier de sortie
    """
    if not cours:
        print("Aucune cours à sauvegarder.")
        return

    # Utilise les noms de champs du modèle coursDejavascript
    fieldnames = coursDeJavascript.model_fields.keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cours)
    print(f"Sauvegarde de {len(cours)} cours dans '{filename}'.")
