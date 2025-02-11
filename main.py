import asyncio

from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv

from config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
from utils.data_utils import (
    save_salles_sport_to_csv,
)
from utils.scraper_utils import (
    fetch_and_process_page,
    get_browser_config,
    get_llm_strategy,
)

load_dotenv()


async def crawl_salles_sport():
    """
    Fonction principale pour crawler les données des salles de sport depuis le site web.
    """
    # Initialisation des configurations
    browser_config = get_browser_config()
    llm_strategy = get_llm_strategy()
    session_id = "salle_sport_crawl_session"

    # Initialisation des variables d'état
    numero_page = 1
    toutes_salles = []
    noms_vus = set()

    # Démarrage du contexte du web crawler
    # https://docs.crawl4ai.com/api/async-webcrawler/#asyncwebcrawler
    async with AsyncWebCrawler(config=browser_config) as crawler:
        while True:
            # Récupération et traitement des données de la page courante
            salles, aucun_resultat = await fetch_and_process_page(
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
                print("Plus de salles de sport trouvées. Fin du crawl.")
                break  # Arrêt du crawl quand le message "Aucun Résultat Trouvé" apparaît

            if not salles:
                print(f"Aucune salle de sport extraite de la page {numero_page}.")
                break  # Arrêt si aucune salle n'est extraite

            # Ajout des salles de cette page à la liste totale
            toutes_salles.extend(salles)
            numero_page += 1  # Passage à la page suivante

            # Pause entre les requêtes pour être poli et éviter les limites de taux
            await asyncio.sleep(6)  # Ajustez le temps de pause selon les besoins

    # Sauvegarde des salles collectées dans un fichier CSV
    if toutes_salles:
        save_salles_sport_to_csv(toutes_salles, "salles_sport_completes.csv")
        print(f"Sauvegarde de {len(toutes_salles)} salles dans 'salles_sport_completes.csv'.")
    else:
        print("Aucune salle de sport n'a été trouvée pendant le crawl.")

    # Affichage des statistiques d'utilisation pour la stratégie LLM
    llm_strategy.show_usage()


async def main():
    """
    Point d'entrée du script.
    """
    await crawl_salles_sport()


if __name__ == "__main__":
    asyncio.run(main())
