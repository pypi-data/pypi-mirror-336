# 📖 mydeen

**mydeen** est un package Python qui, par la permission d’Allah ﷻ, vise à faciliter l’accès aux ressources islamiques (Coran, chaînes YouTube éducatives) pour la communauté francophone.

---

## ✨ Fonctionnalités

- 📚 Accès aux **données du Coran** (sourates, versets, métadonnées…)
- 🧠 Gestion des **parties traditionnelles du Coran** pour la mémorisation (`Hifz`)
- 🔍 Recherche et filtrage par critères (ex: nombre de versets, type de révélation…)
- 📺 Intégration avec **YouTube API** :
  - Récupération des identifiants de chaînes à partir de leurs handles
  - Extraction des playlists d’une chaîne
  - Liste des vidéos d’une playlist
- 🧩 Typages stricts (`TypedDict`, `NamedTuple`, `Enum`) pour plus de fiabilité
- ✅ Zéro dépendance inutile — code léger et structuré

---

## 🔧 Installation

```bash
pip install mydeen
```

> ⚠️ Python **3.9 ou supérieur** requis

---

## 🧪 Exemple d'utilisation

### ✅ Initialisation

```python
from mydeen import MyDeen

mydeen = MyDeen()
```

---

### 📚 1. Accéder aux métadonnées des sourates

```python
surahs = mydeen.meta_surahs().get_all()
```

### 🔍 2. Filtrer des sourates par type de révélation

```python
medinoises = mydeen.meta_surahs().get_by("revelation_type", ["Medinoise"])
```

---

### 🧠 3. Parties du Coran pour la mémorisation (Hifz)

```python
from mydeen import MemoryQuran, PartsNameEnum

memory = MemoryQuran()

# Accéder aux sourates de la partie 'al_mufassal'
part = memory.get_parts(PartsNameEnum.al_mufassal)

# Récupérer les noms des sourates
noms = memory.get_surah_names(PartsNameEnum.al_mufassal)
```

---

### 📺 4. YouTube : chaînes, playlists et vidéos

```python
from mydeen import YoutubeServices, Config

yt = YoutubeServices(api_key="VOTRE_CLE_API")
channel_id = yt.channels.lecoransimplement
playlists = yt.get_playlist(channel_id)
videos = yt.get_videos_playlist(playlists[0]['id'])
```

---

## 📁 Structure du package

```
mydeen/
├── config.py
├── exception_error.py
├── interface.py
├── memory_quran.py
├── metasurahs.py
├── meta_quran_reader.py
├── mydeen.py
├── yt_services.py
└── ...
```

---

## 🤝 Contribuer

Toute contribution utile est la bienvenue, qu’il s’agisse de correction, documentation ou nouvelles fonctionnalités.

---

## 📜 Licence

Ce projet est sous licence **MIT** — Faites-en bon usage et avec sincérité.

---

## 🕋 Intention

> _"Les actions ne valent que par les intentions."_  
> — Hadith authentique (rapporté par Al-Bukhari & Muslim)

Ce projet a été initié dans le but de propager la science bénéfique et l'amour du Coran. Qu’Allah accepte 🌙

---

## 🧑 Auteur

Développé avec foi par **YassinePaquitoNobody**  
📧 Contact : monsieurnobody01@gmail.com  
🔗 [Mon GitHub](https://github.com/YassineNobody)
