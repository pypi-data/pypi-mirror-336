from .metasurahs import MetaSurahs
from .meta_quran_reader import MetaQuranReader
from .yt_services import YoutubeServices
from .memory_quran import MemoryQuran
from .config import Config
from pathlib import Path


class MyDeen:
    """
    Point d'entrée principal du package `mydeen`.
    Fournit l'accès aux différents services liés au Coran, YouTube et mémorisation.
    """

    def __init__(self):
        path = Path(__file__).parent / "data"
        path.mkdir(parents=True, exist_ok=True)
        self.path_database = path.as_posix()
        self.setup_all()

    def config_url(self) -> Config:
        """Retourne la configuration des URLs de ressources utilisées."""
        return Config()

    def meta_surahs(self) -> MetaSurahs:
        """Retourne les métadonnées des sourates du Coran."""
        return MetaSurahs(self.path_database)

    def memory_quran(self) -> MemoryQuran:
        """Retourne l'outil de gestion des parties du Coran à mémoriser."""
        return MemoryQuran()

    def quran_reader(self) -> MetaQuranReader:
        """Retourne un lecteur du texte du Coran avec métadonnées."""
        return MetaQuranReader(self.path_database)

    def yt_services(self, api_key: str) -> YoutubeServices:
        """Retourne un service de récupération des vidéos YouTube."""
        return YoutubeServices(api_key)

    def setup_all(self) -> None:
        """Initialise les fichiers et les données nécessaires (cache, CSV, etc.)."""
        self.meta_surahs()
        self.quran_reader()
