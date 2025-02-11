import csv

from models.salle_sport import SalleDeSport


def is_duplicate_salle(nom_salle: str, noms_vus: set) -> bool:
    """
    Vérifie si une salle de sport est un doublon.
    
    Args:
        nom_salle: Nom de la salle à vérifier
        noms_vus: Ensemble des noms déjà vus
        
    Returns:
        bool: True si la salle est un doublon, False sinon
    """
    return nom_salle in noms_vus


def is_complete_salle(salle: dict, required_keys: list) -> bool:
    """
    Vérifie si une salle de sport contient toutes les informations requises.
    
    Args:
        salle: Dictionnaire contenant les informations de la salle
        required_keys: Liste des clés requises
        
    Returns:
        bool: True si la salle est complète, False sinon
    """
    return all(key in salle for key in required_keys)


def save_salles_sport_to_csv(salles: list, filename: str):
    """
    Sauvegarde la liste des salles de sport dans un fichier CSV.
    
    Args:
        salles: Liste des salles de sport à sauvegarder
        filename: Nom du fichier de sortie
    """
    if not salles:
        print("Aucune salle à sauvegarder.")
        return

    # Utilise les noms de champs du modèle SalleDeSport
    fieldnames = SalleDeSport.model_fields.keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(salles)
    print(f"Sauvegarde de {len(salles)} salles dans '{filename}'.")
