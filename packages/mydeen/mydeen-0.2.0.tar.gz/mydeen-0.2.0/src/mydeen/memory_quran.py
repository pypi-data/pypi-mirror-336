from typing import NamedTuple, TypedDict, Dict, List
from enum import Enum
from .metasurahs import MetaSurahs, ListMetaSurahs
import pandas as pd


class MemoryQuranData(NamedTuple):
    """
    Représente une plage de sourates du Coran à mémoriser.

    Attributs :
        start (int) : Numéro de la sourate de début.
        end (int) : Numéro de la sourate de fin.
    """
    start: int
    end: int


class PartsNameEnum(str, Enum):
    as_sab_u_t_tiwal = "as_sab_u_t_tiwal"
    al_miin = "al_miin"
    al_mathani = "al_mathani"
    al_mufassal = "al_mufassal"
    mufassal_tiwal = "mufassal_tiwal"
    mufassal_awsat = "mufassal_awsat"
    mufassal_qisar = "mufassal_qisar"

    def label(self) -> str:
        return {
            PartsNameEnum.as_sab_u_t_tiwal: "Les 7 longues",
            PartsNameEnum.al_miin: "Les Miin",
            PartsNameEnum.al_mathani: "Les Mathani",
            PartsNameEnum.al_mufassal: "Le Mufassal",
            PartsNameEnum.mufassal_tiwal: "Mufassal Long",
            PartsNameEnum.mufassal_awsat: "Mufassal Moyen",
            PartsNameEnum.mufassal_qisar: "Mufassal Court",
        }[self]


class PartsMemoryQuranData(TypedDict):
    as_sab_u_t_tiwal: MemoryQuranData
    al_miin: MemoryQuranData
    al_mathani: MemoryQuranData
    al_mufassal: MemoryQuranData
    mufassal_tiwal: MemoryQuranData
    mufassal_awsat: MemoryQuranData
    mufassal_qisar: MemoryQuranData


class MemoryParts:
    """
    Contient les différentes sections traditionnelles du Coran
    utilisées dans la mémorisation (hifz).
    """

    @property
    def as_sab_u_t_tiwal(self) -> MemoryQuranData:
        """
        Les 7 longues sourates du Coran.
        Traditionnellement, cela inclut les sourates 2 à 9, même si certains savants
        discutent l'inclusion de la sourate 9 (At-Tawbah).
        """
        return MemoryQuranData(start=2, end=9)

    @property
    def al_miin(self) -> MemoryQuranData:
        """
        Les sourates de longueur moyenne entre les longues et les Mathani.
        Sourates 10 à 33.
        """
        return MemoryQuranData(start=10, end=33)

    @property
    def al_mathani(self) -> MemoryQuranData:
        """
        Les sourates "répétées", plus courtes, souvent riches en exhortations.
        Sourates 34 à 49.
        """
        return MemoryQuranData(start=34, end=49)

    @property
    def al_mufassal(self) -> MemoryQuranData:
        """
        Les sourates très souvent récitées par le Prophète ٠.
        Elles sont en général courtes et commencent à la sourate Qaf (50).
        Sourates 50 à 114.
        """
        return MemoryQuranData(start=50, end=114)

    @property
    def mufassal_tiwal(self) -> MemoryQuranData:
        """
        Partie longue du Mufassal.
        Sourates 50 à 77.
        """
        return MemoryQuranData(start=50, end=77)

    @property
    def mufassal_awsat(self) -> MemoryQuranData:
        """
        Partie moyenne du Mufassal.
        Sourates 78 à 92.
        """
        return MemoryQuranData(start=78, end=92)

    @property
    def mufassal_qisar(self) -> MemoryQuranData:
        """
        Partie courte du Mufassal.
        Très souvent mémorisée en premier par les enfants.
        Sourates 93 à 114.
        """
        return MemoryQuranData(start=93, end=114)

    @property
    def all_parts(self) -> PartsMemoryQuranData:
        return {
            "as_sab_u_t_tiwal": self.as_sab_u_t_tiwal,
            "al_miin": self.al_miin,
            "al_mathani": self.al_mathani,
            "al_mufassal": self.al_mufassal,
            "mufassal_tiwal": self.mufassal_tiwal,
            "mufassal_awsat": self.mufassal_awsat,
            "mufassal_qisar": self.mufassal_qisar,
        }


class MemoryQuran:
    def __init__(self) -> None:
        self._quran = MetaSurahs()
        self._memory_parts = MemoryParts()

    def get_parts(self, part: PartsNameEnum, respapi: bool = True):
        memory_parts = self._memory_parts.all_parts[part.value]
        memory_parts_with_surahs = self._quran.get_surahs(
            memory_parts.start, memory_parts.end
        )
        return (
            memory_parts_with_surahs
            if respapi
            else pd.DataFrame(memory_parts_with_surahs)
        )

    def get_all_parts(self, respapi: bool = True) -> Dict[PartsNameEnum, ListMetaSurahs]:
        return {
            part: self.get_parts(part, respapi=respapi)
            for part in PartsNameEnum
        }

    def get_surah_names(self, part: PartsNameEnum) -> List[str]:
        return self.get_parts(part)["name_french"].tolist()

    def get_keywords_learning_methods(self) -> List[str]:
        return [e.value for e in PartsNameEnum]
