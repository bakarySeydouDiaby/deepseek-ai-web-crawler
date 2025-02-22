import json
import os
from typing import List, Set, Tuple
import asyncio

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig, 
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
)

from models.cours_javascript import coursDeJavascript
from utils.data_utils import is_complete_cours, is_duplicate_cours


def get_browser_config() -> BrowserConfig:
    """Configure le navigateur pour le crawling"""
    return BrowserConfig(
        browser_type="chromium",  # Type de navigateur à simuler
        headless=False,  # Mode sans interface graphique
        verbose=True,  # Active les logs détaillés
    )


def get_llm_strategy() -> LLMExtractionStrategy:
    """Configure la stratégie d'extraction par LLM"""
    return LLMExtractionStrategy(
        provider="groq/deepseek-r1-distill-llama-70b",  # Fournisseur du modèle LLM
        api_token=os.getenv("GROQ_API_KEY"),  # Token d'API pour l'authentification
        schema=coursDeJavascript.model_json_schema(),  # Schéma JSON du modèle de données
        extraction_type="schema",  # Type d'extraction à effectuer
        instruction=(
            "Extrait tous les cours de javascript avec les données 'title', 'skills', 'description', 'reviews', 'rating'"
        ),  # Instructions pour le LLM
        input_format="markdown",  # Format du contenu d'entrée
        verbose=True,  # Active les logs détaillés
    )


async def check_no_results(
    crawler: AsyncWebCrawler,
    url: str,
    session_id: str,
) -> bool:
    """Vérifie si la page indique qu'aucun résultat n'a été trouvé"""
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            session_id=session_id,
        ),
    )

    if result.success:
        if "Désolés, nous n'avons pas ça sous la main !" in result.cleaned_html:
            return True
    else:
        print(
            f"Erreur lors de la vérification de la page pour 'Aucun résultat': {result.error_message}"
        )

    return False


async def fetch_and_process_page(
    crawler: AsyncWebCrawler,
    numero_page: int,
    base_url: str,
    css_selector: str,
    llm_strategy: LLMExtractionStrategy,
    session_id: str,
    required_keys: List[str],
    noms_vus: Set[str],
) -> Tuple[List[dict], bool]:
    """Récupère et traite une page de résultats"""

    url = f"{base_url}&page={numero_page}"
    print(f"Chargement de la page {numero_page}...")

    await asyncio.sleep(6)  # Temps de pause ajustable

    # Vérifie si le message "Aucun résultat" est présent
    aucun_resultat = await check_no_results(crawler, url, session_id)
    if aucun_resultat:
        return [], True  # Plus de résultats, signal d'arrêt du crawling

    # Récupère le contenu de la page avec la stratégie d'extraction
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,  # N'utilise pas le cache
            extraction_strategy=llm_strategy,  # Stratégie d'extraction
            css_selector=css_selector,  # Sélecteur CSS pour cibler le contenu
            session_id=session_id,  # ID unique pour la session de crawl
        ),
    )

    if not (result.success and result.extracted_content):
        print(f"Erreur lors de la récupération de la page {numero_page}: {result.error_message}")
        return [], False

    # Parse le contenu extrait
    donnees_extraites = json.loads(result.extracted_content)
    if not donnees_extraites:
        print(f"Aucun cours de javascript trouvé sur la page {numero_page}.")
        return [], False

    # Après l'analyse du contenu extrait
    print("Données extraites:", donnees_extraites)

    # Traitement des cours
    cours_complets = []
    for cours in donnees_extraites:
        # Debug: Affiche chaque cours pour comprendre sa structure
        print("Traitement de la cours:", cours)

        # Ignore la clé 'error' si elle est False
        if cours.get("error") is False:
            cours.pop("error", None)  # Supprime la clé 'error' si False

        if not is_complete_cours(cours, required_keys):
            continue  # Ignore les courss incomplètes

        if is_duplicate_cours(cours["title"], noms_vus):
            print(f"cours en double '{cours['title']}' trouvée. Ignorée.")
            continue  # Ignore les doublons

        # Ajoute la cours à la liste
        noms_vus.add(cours["title"])
        cours_complets.append(cours)

    if not cours_complets:
        print(f"Aucune cours complète trouvée sur la page {numero_page}.")
        return [], False

    print(f"Extraction de {len(cours_complets)} courss de la page {numero_page}.")
    return cours_complets, False  # Continue le crawling
