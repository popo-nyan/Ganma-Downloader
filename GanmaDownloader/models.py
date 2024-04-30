from dataclasses import dataclass
from enum import Enum


class ApolloOperation(Enum):
    MagazineStoryReaderQuery = "60dae270d44f863e2f485a7fffe83abb5a1d6e3c4fea394e048524ca81c64ca8"
    SearchComic = "2fb9fce5650a48d520ff6cbf6bf6d5edd6e5ea6af3a139212d2b13134c2344a4"


@dataclass(slots=True)
class CreateAccountResponseModel:
    user_id: str
    password: str


@dataclass(slots=True)
class AnnounceTransitionBaseModel:
    destinationURL: str | None = None
    way: str | None = None


@dataclass(slots=True)
class AnnounceCementBaseModel:
    test: str | None = None


@dataclass(slots=True)
class AuthorBaseModel:
    name: str
    profile_image_url: str | None
    profile_text: str | None
    author_link: dict | None = None


@dataclass(slots=True)
class MagazineItemBaseModel:
    disableCm: bool | None = None
    hasExchange: bool = None
    heartCount: int = None
    kind: str = None
    number: int = None
    releaseStart: int = None
    seriesTitle: str = None
    storyId: str = None
    subtitle: str | None = None
    thumbnailImageUrl: str = None
    title: str = None


@dataclass(slots=True)
class MagazineResponseModel:
    alias: str
    author: AuthorBaseModel
    bookmark_count: int
    can_accept_fan_letter: bool
    can_support: bool
    description: str
    distribution_label: str
    heart_count: int
    id: str
    is_gtoon: bool
    is_series_bind: bool
    stories: list[MagazineItemBaseModel]
    overview: str | None
    public_latest_story_number: int
    rectangle_with_logo_image_url: str
    story_release_status: str | None
    title: str
    upcoming: dict | None = None
    first_view_advertisements: list[dict] | None = None
    footer_advertisements: list[dict] | None = None
    highlight_image_urls: list[str] | None = None
    recommendations: list | None = None
    related_link: list | None = None
    tags: list[dict] | None = None


@dataclass(slots=True)
class MagazineBaseModel:
    magazine_id: str
    title: str
    alias: str
    overview: str
    authr: AuthorBaseModel | None = None


@dataclass(slots=True)
class StoryInfoBaseModel:
    story_id: str
    title: str
    subtitle: str | None = None


@dataclass(slots=True)
class PageImageBaseModel:
    secret_key: str | None = None
    page_image_base_url: str | None = None
    page_image_sign: str | None = None
    page_count: int | None = None


@dataclass(slots=True)
class StoryContentBaseModel:
    story_info: StoryInfoBaseModel | None = None
    page_images: PageImageBaseModel | None = None


@dataclass(slots=True)
class MagazineStoryReaderResponseModel:
    magazine_id: str
    story_contents: StoryContentBaseModel | None = None


@dataclass(slots=True)
class SearchComicResponseBaseModel:
    type_name: str
    title: str
    magazine_id: str
    author_name: str
    todays_jacket_image_url: str | None = None
