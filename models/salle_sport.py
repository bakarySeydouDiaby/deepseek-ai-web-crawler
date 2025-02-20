from pydantic import BaseModel


class SalleDeSport(BaseModel):
    """
    Représente la structure de données d'une salle de sport.
    """

    nom: str  # Nom de la salle de sport
    adresse: str  # Adresse complète de la salle
    description: str  # Description détaillée de la salle et de ses services
    note: str  # Note moyenne attribuée par les utilisateurs
    lien_annonce: int  # Identifiant unique de l'annonce sur le site
