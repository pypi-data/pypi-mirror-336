import json
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
from typing_extensions import TypedDict

from mydeen.yt_services_processor import (
    YoutubeServicesProcessorCache,
    Channels,
    NameChannels,
    Playlist,
    Video,
)


class CacheJSON(TypedDict):
    channel_ids: Channels
    channels: NameChannels
    playlists: Dict[str, List[Playlist]]
    videos: Dict[str, List[Video]]
    last_update: str  # Format ISO 8601


class YoutubeServices:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.__yt_processor = YoutubeServicesProcessorCache(api_key)
        self.path_cache = Path(__file__).parent / "data" / "cache_yt.json"
        self.path_cache.parent.mkdir(parents=True, exist_ok=True)
        self.__cache = None

        if not self.path_cache.exists() or self._is_cache_empty():
            print("📂 Cache inexistant ou vide, création/mise à jour...")
            self.update_cache()

    def _is_cache_empty(self) -> bool:
        try:
            with open(self.path_cache, "r", encoding="utf-8") as f:
                return not bool(json.load(f))
        except Exception:
            return True

    def update_cache(self) -> None:
        """
        Met à jour le cache local avec les données des chaînes, playlists et vidéos.
        """
        print("🔄 Mise à jour du cache YouTube...")

        channel_ids = self.__yt_processor.connect_id_channels()
        channel_names = self.__yt_processor.connect_title_channels()
        playlists: Dict[str, List[Playlist]] = {}
        videos: Dict[str, List[Video]] = {}

        for key, channel_id in channel_ids._asdict().items():
            try:
                print(f"📺 Récupération des playlists pour la chaîne : {key}")
                channel_playlists = self.__yt_processor.get_playlist(channel_id)
                playlists[key] = channel_playlists

                for playlist in channel_playlists:
                    playlist_id = playlist["id"]
                    print(f"🎞️  → Récupération des vidéos de la playlist {playlist_id}")
                    playlist_videos = self.__yt_processor.get_videos_playlist(
                        playlist_id
                    )
                    videos[playlist_id] = playlist_videos

            except Exception as e:
                print(f"⚠️ Erreur lors de la récupération de {key}: {e}")

        cache_data: CacheJSON = {
            "channel_ids": channel_ids,
            "channels": channel_names,
            "playlists": playlists,
            "videos": videos,
            "last_update": datetime.utcnow().isoformat(),
        }

        with open(self.path_cache, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=4)

        print("✅ Cache YouTube mis à jour avec succès !")

    def __read_cache(self) -> CacheJSON:
        with open(self.path_cache, "r") as f:
            return json.load(f)

    @property
    def cache(self) -> CacheJSON:
        if self.__cache is None:
            self.__cache = self.__read_cache()
        return self.__cache

    def get_channels(self) -> NameChannels:
        return self.cache["channels"]

    def get_channel_ids(self) -> Channels:
        return self.cache["channel_ids"]

    def get_playlists(self, channel_key: str) -> List[Playlist]:
        return self.cache["playlists"].get(channel_key, [])

    def get_videos_from_playlist(self, playlist_id: str) -> List[Video]:
        return self.cache["videos"].get(playlist_id, [])

    @property
    def last_update(self) -> datetime:
        try:
            return datetime.fromisoformat(self.cache["last_update"])
        except Exception:
            return datetime.min

    def is_cache_expired(self, hours: int = 24) -> bool:
        try:
            return datetime.utcnow() - self.last_update > timedelta(hours=hours)
        except Exception:
            return True

    def refresh_cache(
        self, force: bool = False, async_mode: bool = True, hours: int = 24
    ) -> None:
        if force or self._is_cache_empty() or self.is_cache_expired(hours):
            print("♻️ Rafraîchissement du cache YouTube...")
            if async_mode:
                threading.Thread(target=self.update_cache, daemon=True).start()
            else:
                self.update_cache()

    def __repr__(self):
        return (
            f"<YoutubeServices last_update={self.cache.get('last_update', 'unknown')}>"
        )
