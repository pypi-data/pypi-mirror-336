from typing import Any, NamedTuple, List, Dict, Optional
from typing_extensions import TypedDict
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .config import Config

class Channels(NamedTuple):
    lislamsimplement: str
    larabesimplement: str
    lecoransimplement: str


class NameChannels(NamedTuple):
    lislamsimplement: str
    larabesimplement: str
    lecoransimplement: str


class Playlist(TypedDict):
    title: str
    id: str
    video_count: int
    thumbnail: str
    url_playlist: str
    description: str


class Video(TypedDict):
    title: str
    video_id: str
    position: int
    published_at: str
    thumbnail: str
    url: str


class YoutubeServicesProcessorCache:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.youtube: Any = build(
            "youtube", "v3", developerKey=api_key, cache_discovery=False
        )
        self.handles = Config.handles_yt()

    def __repr__(self) -> str:
        return f"<YoutubeServices connected with key=****{self.api_key[-4:]}>"

    def __get_channel_data(self, handle: str) -> Optional[Dict[str, Any]]:
        try:
            req = self.youtube.search().list(
                part="snippet", type="channel", q=handle, maxResults=1
            )
            res = req.execute()
            return res["items"][0] if res["items"] else None
        except HttpError as e:
            raise e

    def get_channel_id(self, handle: str) -> Optional[str]:
        data = self.__get_channel_data(handle)
        return data["snippet"].get("channelId") if data else None

    def get_name_channel_id(self, handle: str) -> Optional[str]:
        data = self.__get_channel_data(handle)
        return data["snippet"].get("title") if data else None

    def connect_title_channels(self) -> NameChannels:
        channels = {
            k: self.get_name_channel_id(v) for k, v in self.handles._asdict().items()
        }
        return NameChannels(**channels)

    def connect_id_channels(self) -> Channels:
        channels = {
            k: self.get_channel_id(v) for k, v in self.handles._asdict().items()
        }
        return Channels(**channels)

    def get_playlist(self, channel_id: str) -> List[Playlist]:
        playlists = []
        next_page_token = None
        while True:
            req = self.youtube.playlists().list(
                part="snippet, contentDetails",
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token,
            )
            res = req.execute()
            playlists.extend(res.get("items", []))
            next_page_token = res.get("nextPageToken")
            if not next_page_token:
                break
        return self.__parser_playlist(playlists)

    def __parser_playlist(self, playlists: List[Dict[str, Any]]) -> List[Playlist]:
        data = []
        for playlist in playlists:
            snippet = playlist.get("snippet", {})
            content = playlist.get("contentDetails", {})
            data.append(
                {
                    "title": snippet.get("title", ""),
                    "id": playlist.get("id", ""),
                    "video_count": content.get("itemCount", 0),
                    "thumbnail": snippet.get("thumbnails", {})
                    .get("medium", {})
                    .get("url", ""),
                    "url_playlist": f"https://www.youtube.com/playlist?list={playlist.get('id', '')}",
                    "description": snippet.get("description", ""),
                }
            )
        return data

    def get_videos_playlist(self, playlist_id: str) -> List[Video]:
        videos = []
        next_page_token = None
        while True:
            req = self.youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token,
            )
            res = req.execute()
            videos.extend(res.get("items", []))
            next_page_token = res.get("nextPageToken")
            if not next_page_token:
                break
        return self.__parser_videos(videos, playlist_id)

    def __parser_videos(
        self, videos: List[Dict[str, Any]], playlist_id: str
    ) -> List[Video]:
        data = []
        for video in videos:
            snippet = video.get("snippet", {})
            resource = snippet.get("resourceId", {})
            video_id = resource.get("videoId", "")
            data.append(
                {
                    "title": snippet.get("title", ""),
                    "video_id": video_id,
                    "position": snippet.get("position", 0),
                    "published_at": snippet.get("publishedAt", ""),
                    "thumbnail": snippet.get("thumbnails", {})
                    .get("medium", {})
                    .get("url", ""),
                    "url": f"https://www.youtube.com/watch?v={video_id}&list={playlist_id}",
                }
            )
        return data


