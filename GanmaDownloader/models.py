from pydantic import BaseModel as PydanticBaseModel
from typing import Optional, List


class CreateAccountResponseBase(PydanticBaseModel):
    id: str
    password: str


class AnnounceTransitionBase(PydanticBaseModel):
    destinationURL: Optional[str] = None
    way: Optional[str] = None


class AnnounceCementBase(PydanticBaseModel):
    test: Optional[str] = None


class AuthorBase(PydanticBaseModel):
    link: Optional[dict] = None
    name: str
    profileImageURL: Optional[str]
    profileText: Optional[str]


class MagazineItemBase(PydanticBaseModel):
    disableCM: bool = None
    hasExchange: bool = None
    heartCount: int = None
    kind: str = None
    number: int = None
    releaseStart: int = None
    seriesTitle: str = None
    storyId: str = None
    subtitle: str = None
    thumbnailImageURL: str = None
    title: str = None


class MagazineModel(PydanticBaseModel):
    alias: str
    author: AuthorBase
    bookmarkCount: int
    canAcceptFanLetter: bool
    canSupport: bool
    description: str
    distributionLabel: str
    firstViewAdvertisements: Optional[List[dict]] = None
    footerAdvertisements: Optional[List[dict]] = None
    heartCount: int
    highlightImageURLs: Optional[List[str]] = None
    id: str
    isGTOON: bool
    isSeriesBind: bool
    items: List[MagazineItemBase]
    overview: Optional[str]
    publicLatestStoryNumber: int
    recommendations: Optional[list] = None
    rectangleWithLogoImageURL: str
    relatedLink: Optional[dict] = None
    storyReleaseStatus: Optional[str]
    tags: Optional[List[dict]] = None
    title: str
    upcoming: Optional[dict] = None
