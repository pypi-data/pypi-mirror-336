from pathlib import Path
from typing import Union, Optional

from .metasurahs import MetaSurahs, LanguageOptions
from .meta_quran_reader import MetaQuranReader
from .yt_services import YoutubeServices
from .memory_quran import MemoryQuran
from .config import Config


class MyDeen:
    """
    Point d'entrée principal du package `mydeen`.
    Fournit l'accès aux différents services liés au Coran, YouTube et mémorisation.
    """

    def __init__(
        self,
        language: Optional[LanguageOptions] = None,
        api_key: Optional[str] = None,
    ) -> None:
        path = Path(__file__).parent / "data"
        path.mkdir(parents=True, exist_ok=True)
        self.path_database = path.as_posix()

        self.__language = (
            MetaSurahs(self.path_database, language).language if language else None
        )
        self.__api_key = api_key
        self.__yt_service_instance: Optional[YoutubeServices] = None

        self.setup_all()

    @property
    def language(self) -> Optional[LanguageOptions]:
        return self.__language

    def config_url(self) -> Config:
        """Retourne la configuration des URLs de ressources utilisées."""
        return Config()

    def meta_surahs(self, language: Optional[LanguageOptions] = None) -> MetaSurahs:
        """Retourne les métadonnées des sourates du Coran."""
        lang = language or self.__language
        return (
            MetaSurahs(self.path_database, lang)
            if lang
            else MetaSurahs(self.path_database)
        )

    def memory_quran(self) -> MemoryQuran:
        """Retourne l'outil de gestion des parties du Coran à mémoriser."""
        return MemoryQuran()

    def quran_reader(self) -> MetaQuranReader:
        """Retourne un lecteur du texte du Coran avec métadonnées."""
        return MetaQuranReader(self.path_database)

    def yt_services(
        self,
        api_key: Optional[str] = None,
        refresh_cache_auto: bool = False,
        hours: int = 24,
    ) -> YoutubeServices:
        """Retourne un service de récupération des vidéos YouTube avec cache."""
        if self.__yt_service_instance:
            return self.__yt_service_instance

        key = api_key or self.__api_key
        if not key:
            raise ValueError(
                "Une clé API est requise pour utiliser les services YouTube."
            )

        yt_service = YoutubeServices(key)
        if refresh_cache_auto:
            yt_service.refresh_cache(async_mode=True, hours=hours)
        self.__yt_service_instance = yt_service
        return yt_service

    def setup_all(self) -> dict:
        """Initialise les fichiers et données (cache, CSV, etc.)."""
        setup_info = {
            "meta_surahs": self.meta_surahs(),
            "quran_reader": self.quran_reader(),
        }
        if self.__api_key:
            setup_info["yt_services"] = self.yt_services()
        return setup_info
