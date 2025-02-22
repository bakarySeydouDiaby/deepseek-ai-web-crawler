import asyncio

from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv

from config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
from utils.data_utils import (
    save_cours_javascript_to_csv,
)

from utils.scraper_utils import (
    fetch_and_process_page,
    get_browser_config,
    get_llm_strategy,
)

load_dotenv()


async def test_crawl_coursera():
    """
    Fonction principale pour crawler les données des cours de javascript depuis le site web.
    """
    # Initialisation des configurations
    browser_config = get_browser_config()
    llm_strategy = get_llm_strategy()
    session_id = "javascript_courses_crawl_session"

    # Initialisation des variables d'état
    numero_page = 1
    tous_les_cours = []
    noms_vus = set()

    # Démarrage du contexte du web crawler
    # https://docs.crawl4ai.com/api/async-webcrawler/#asyncwebcrawler
    async with AsyncWebCrawler(config=browser_config) as crawler:
        while True:
            # Récupération et traitement des données de la page courante
            cours, aucun_resultat = await fetch_and_process_page(
                crawler,
                numero_page,
                BASE_URL,
                CSS_SELECTOR,
                llm_strategy,
                session_id,
                REQUIRED_KEYS,
                noms_vus,
            )

            if aucun_resultat:
                print("Plus de cours de javascript trouvées. Fin du crawl.")
                break  # Arrêt du crawl quand le message "Aucun Résultat Trouvé" apparaît

            if not cours:
                print(f"Aucun cours de javascript extraite de la page {numero_page}.")
                break  # Arrêt si aucune cours n'est extraite

            # Ajout des cours de cette page à la liste totale
            tous_les_cours.extend(cours)
            numero_page += 1  # Passage à la page suivante

            # Pause entre les requêtes pour être poli et éviter les limites de taux
            await asyncio.sleep(6)  # Ajustez le temps de pause selon les besoins

    # Sauvegarde des cours collectées dans un fichier CSV
    if tous_les_cours:
        save_cours_javascript_to_csv(tous_les_cours, "cours_javascript_completes.csv")
        print(f"Sauvegarde de {len(tous_les_cours)} cours dans 'cours_javascript_completes.csv'.")
    else:
        print("Aucune cours de javascript n'a été trouvée pendant le crawl.")

    # Affichage des statistiques d'utilisation pour la stratégie LLM
    llm_strategy.show_usage()


async def main():
    """
    Point d'entrée du script.
    """
    await test_crawl_coursera()


if __name__ == "__main__":
    asyncio.run(main())
