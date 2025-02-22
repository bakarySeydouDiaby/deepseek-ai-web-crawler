from pydantic import BaseModel


class coursDeJavascript(BaseModel):
    """
    Représente la structure de données d'un cours de javascript.
    """
    title: str  # Titre du cours
    skills: str  # Compétences enseignées
    description: str  # Description du cours
    reviews: str  # Nombre d'avis
    rating: str  # Note moyenne attribuée par les utilisateurs
