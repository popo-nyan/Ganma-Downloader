from dataclasses import dataclass


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
    disable_cm: bool | None = None
    has_exchange: bool = None
    heart_count: int = None
    kind: str = None
    number: int = None
    release_start: int = None
    series_title: str = None
    story_id: str = None
    subtitle: str | None = None
    thumbnail_image_url: str = None
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
    items: list[MagazineItemBaseModel]
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
class MagazineStoryReaderResponseModel:
    magazine_id: str
