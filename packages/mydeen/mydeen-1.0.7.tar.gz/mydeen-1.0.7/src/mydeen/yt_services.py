import json
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, TypedDict

from mydeen.yt_services_processor import (
    YoutubeServicesProcessorCache,
    Playlist,
    Video,
)


class ChannelInfo(TypedDict):
    id: str
    name: str


class CacheJSON(TypedDict):
    channels: Dict[str, ChannelInfo]  # handle -> {id, name}
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
        print("🔄 Mise à jour du cache YouTube...")

        handles = self.__yt_processor.handles._asdict()
        channels: Dict[str, ChannelInfo] = {}
        playlists: Dict[str, List[Playlist]] = {}
        videos: Dict[str, List[Video]] = {}

        for handle, username in handles.items():
            try:
                print(f"🔍 Récupération pour {handle} (@{username})")
                channel_id = self.__yt_processor.get_channel_id(username)
                channel_name = self.__yt_processor.get_name_channel_id(username)

                if not channel_id or not channel_name:
                    raise ValueError("ID ou nom de chaîne manquant")

                channels[handle] = {"id": channel_id, "name": channel_name}

                print(f"📺 Récupération des playlists pour la chaîne : {channel_name}")
                channel_playlists = self.__yt_processor.get_playlist(channel_id)
                playlists[handle] = channel_playlists

                for playlist in channel_playlists:
                    playlist_id = playlist["id"]
                    print(f"🎞️  → Récupération des vidéos de la playlist {playlist_id}")
                    playlist_videos = self.__yt_processor.get_videos_playlist(
                        playlist_id
                    )
                    videos[playlist_id] = playlist_videos

            except Exception as e:
                print(f"⚠️ Erreur pour {handle}: {e}")

        cache_data: CacheJSON = {
            "channels": channels,
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

    def get_channels(self) -> Dict[str, ChannelInfo]:
        return self.cache["channels"]

    def get_channel_ids(self) -> Dict[str, str]:
        return {k: v["id"] for k, v in self.get_channels().items()}

    def get_channel_names(self) -> Dict[str, str]:
        return {k: v["name"] for k, v in self.get_channels().items()}

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
