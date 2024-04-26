from dataclasses import dataclass


@dataclass(slots=True)
class CreateAccountResponseBase:
    user_id: str
    password: str


@dataclass(slots=True)
class AnnounceTransitionBase:
    destinationURL: str | None = None
    way: str | None = None


@dataclass(slots=True)
class AnnounceCementBase:
    test: str | None = None


@dataclass(slots=True)
class AuthorBase:
    name: str
    profileImageURL: str | None
    profileText: str | None
    author_link: dict | None = None


@dataclass(slots=True)
class MagazineItemBase:
    disableCM: bool | None = None
    hasExchange: bool = None
    heartCount: int = None
    kind: str = None
    number: int = None
    releaseStart: int = None
    seriesTitle: str = None
    storyId: str = None
    subtitle: str | None = None
    thumbnailImageURL: str = None
    title: str = None


@dataclass(slots=True)
class MagazineModel:
    alias: str
    author: AuthorBase
    bookmarkCount: int
    canAcceptFanLetter: bool
    canSupport: bool
    description: str
    distributionLabel: str
    heartCount: int
    id: str
    isGTOON: bool
    isSeriesBind: bool
    items: list[MagazineItemBase]
    overview: str | None
    publicLatestStoryNumber: int
    rectangleWithLogoImageURL: str
    storyReleaseStatus: str | None
    title: str
    upcoming: dict | None = None
    firstViewAdvertisements: list[dict] | None = None
    footerAdvertisements: list[dict] | None = None
    highlightImageURLs: list[str] | None = None
    recommendations: list | None = None
    relatedLink: list | None = None
    tags: list[dict] | None = None
