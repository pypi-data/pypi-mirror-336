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

    def __init__(self, language: str = None) -> None:
        path = Path(__file__).parent / "data"
        path.mkdir(parents=True, exist_ok=True)
        self.path_database = path.as_posix()
        if language:
            self.__language = MetaSurahs(self.path_database, language).language
        else:
            self.__language = None
        self.setup_all()

    @property
    def language(self) -> str:
        return self.__language

    def config_url(self) -> Config:
        """Retourne la configuration des URLs de ressources utilisées."""
        return Config()

    def meta_surahs(self, language: str = None) -> MetaSurahs:
        """Retourne les métadonnées des sourates du Coran."""
        if language is None and self.__language is None:
            return MetaSurahs(self.path_database)
        elif language and self.__language is None:
            return MetaSurahs(self.path_database, language)
        elif language is None and self.__language:
            return MetaSurahs(self.path_database, self.__language)
        else:
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
