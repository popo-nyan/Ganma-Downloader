import uuid
import httpx
from json import dumps
import aiofiles

from .models import CreateAccountResponseModel, MagazineResponseModel, MagazineItemBaseModel, \
    MagazineStoryReaderResponseModel, PageImageBaseModel, StoryInfoBaseModel, StoryContentBaseModel
from .utils import make_directory


class Client:

    def __init__(self):
        self.__session = httpx.AsyncClient(http2=True, headers={
            'Host': 'reader.ganma.jp',
            'User-Agent': 'GanmaReader/9.0.0 Android releaseVersion:12 model:samsung/SC-51D',
            'X-From': 'https://reader.ganma.jp/api/',
            'X-Noescape': 'true',
            'Connection': 'close'})
        self._play_session = ""

    async def create_account(self) -> CreateAccountResponseModel | None:
        create_account_response = await self.__session.post(url="https://reader.ganma.jp/api/1.0/account")
        if create_account_response.status_code == httpx.codes.OK:
            params = {'clientType': 'app',
                      'installationId': str(uuid.uuid4()),
                      'explicit': 'false'}
            data = {"id": create_account_response.json()['root']['id'],
                    "password": create_account_response.json()['root']['password']}
            login_response = await self.__session.post(url="https://reader.ganma.jp/api/3.0/session",
                                                       params=params,
                                                       data=data)
            if login_response.status_code == httpx.codes.OK and login_response.json()['success']:
                self._play_session = login_response.cookies.get("PLAY_SESSION")
                return CreateAccountResponseModel(user_id=data['id'],
                                                  password=data['password'])
        return None

    async def get_magazine_data(self,
                                magazine_alias: str
                                ) -> MagazineResponseModel | None:
        response = await self.__session.get(url=f"https://reader.ganma.jp/api/3.2/magazines/{magazine_alias}")
        if response.status_code == httpx.codes.OK:
            response_json = response.json()['root']
            stories = []
            for story in response_json['items']:
                if story.get("subtitle") is not None:
                    stories.append(MagazineItemBaseModel(storyId=story['storyId'],
                                                         title=story['title'],
                                                         seriesTitle=story['seriesTitle'],
                                                         subtitle=story['subtitle'],
                                                         thumbnailImageUrl=story['thumbnailImageURL'],
                                                         kind=story['kind'],
                                                         releaseStart=story['releaseStart'],
                                                         heartCount=story['heartCount'],
                                                         disableCm=story['disableCM'],
                                                         hasExchange=story['hasExchange']))
                    continue
                else:
                    stories.append(MagazineItemBaseModel(storyId=story['storyId'],
                                                         title=story['title'],
                                                         seriesTitle=story['seriesTitle'],
                                                         thumbnailImageUrl=story['thumbnailImageURL'],
                                                         kind=story['kind'],
                                                         releaseStart=story['releaseStart'],
                                                         heartCount=story['heartCount'],
                                                         disableCm=story['disableCM'],
                                                         hasExchange=story['hasExchange']))

            return MagazineResponseModel(alias=response_json['alias'],
                                         author=response_json['author'],
                                         bookmark_count=response_json['bookmarkCount'],
                                         can_accept_fan_letter=response_json['canAcceptFanLetter'],
                                         can_support=response_json['canSupport'],
                                         description=response_json['description'],
                                         distribution_label=response_json['distributionLabel'],
                                         first_view_advertisements=response_json['firstViewAdvertisements'],
                                         footer_advertisements=response_json['footerAdvertisements'],
                                         heart_count=response_json['heartCount'],
                                         highlight_image_urls=response_json['highlightImageURLs'],
                                         id=response_json['id'],
                                         is_gtoon=response_json['isGTOON'],
                                         is_series_bind=response_json['isSeriesBind'],
                                         stories=stories,
                                         overview=response_json['overview'],
                                         public_latest_story_number=response_json['publicLatestStoryNumber'],
                                         recommendations=response_json['recommendations'],
                                         rectangle_with_logo_image_url=response_json['rectangleWithLogoImageURL'],
                                         related_link=response_json['relatedLink'],
                                         story_release_status=response_json['storyReleaseStatus'],
                                         tags=response_json['tags'],
                                         title=response_json['title'],
                                         upcoming=response_json['upcoming'])

        else:
            return None

    async def get_magazine_story_reader(self,
                                        magazine_alias: str,
                                        story_id: str) -> MagazineStoryReaderResponseModel | None:
        response = await self.__session.get(url="https://ganma.jp/api/graphql",
                                            headers={'Host': 'ganma.jp',
                                                     'X-Apollo-Operation-Id': '60dae270d44f863e2f485a7fffe83abb5a1d6e3c4fea394e048524ca81c64ca8',
                                                     'X-Apollo-Operation-Name': 'MagazineStoryReaderQuery',
                                                     'Accept': 'multipart/mixed; deferSpec=20220824, application/json',
                                                     'User-Agent': 'GanmaReader/9.0.0 Android releaseVersion:12 model:samsung/SC-51D',
                                                     'X-From': 'https://reader.ganma.jp/api/',
                                                     'X-Noescape': 'true'},
                                            params={'operationName': 'MagazineStoryReaderQuery',
                                                    'variables': dumps({'magazineIdOrAlias': magazine_alias,
                                                                        'storyId': story_id,
                                                                        'publicKey': None}),
                                                    'extensions': dumps({'persistedQuery': {'version': 1,
                                                                                            'sha256Hash': '60dae270d44f863e2f485a7fffe83abb5a1d6e3c4fea394e048524ca81c64ca8'}})})
        if response.status_code == httpx.codes.OK and response.json().get("data") is not None:
            response_json = response.json()['data']
            if response_json['magazine'].get("storyContents") is None or response_json['magazine']['storyContents'].get(
                    "storyInfo") is None:
                return None
            return MagazineStoryReaderResponseModel(magazine_id=response_json['magazine']['magazineId'],
                                                    story_contents=StoryContentBaseModel(
                                                        story_info=StoryInfoBaseModel(story_id=
                                                                                      response_json['magazine']
                                                                                      ['storyContents']['storyInfo']
                                                                                      ['storyId'],
                                                                                      title=
                                                                                      response_json['magazine']
                                                                                      ['storyContents']['storyInfo']
                                                                                      ['title'],
                                                                                      subtitle=
                                                                                      response_json['magazine']
                                                                                      ['storyContents']['storyInfo']
                                                                                      ['subtitle']),
                                                        page_images=PageImageBaseModel(
                                                            page_image_base_url=
                                                            response_json['magazine']['storyContents']
                                                            ['pageImages']['pageImageBaseURL'],
                                                            page_image_sign=response_json['magazine']
                                                            ['storyContents']['pageImages']['pageImageSign'],
                                                            page_count=response_json['magazine']['storyContents']
                                                            ['pageImages']['pageCount'])))
        else:
            return None

    async def download_story_image(self,
                                   base_url: str,
                                   image_sign: str,
                                   page_count: int,
                                   alias: str,
                                   title: str,
                                   subtitle: str):
        make_directory(alias.strip("\\?()!@#$%^&*()_+{}?>!"))
        save_image_path = alias.strip("\\?()!@#$%^&*()_+{}?>!") + r"\\" + title.strip("\\?()!@#$%^&*()_+{}?>!") + "-" + subtitle.strip("\\?()!@#$%^&*()_+{}?>!")
        make_directory(save_image_path)
        response = await self.__session.get(url=base_url + str(page_count) + ".jpg?" + image_sign,
                                            headers={'Host': 'd1bzi54d5ruxfk.cloudfront.net',
                                                     'Accept-Encoding': 'gzip, deflate, br',
                                                     'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; SM-G973N Build/PPR1.190810.011)',
                                                     'User-Agent': 'GanmaReader/9.2.0 Android releaseVersion:9 model:samsung/SM-G973N'})
        if response.status_code == httpx.codes.OK:
            async with aiofiles.open(save_image_path + r"\\" + str(page_count) + ".jpg", "wb") as f:
                await f.write(response.content)
            print(f"[INFO] Success download image | {alias} | {title} | {subtitle} | {page_count}")
        else:
            print(f"[ERROR] The image could not be downloaded | {alias} | {title} | {subtitle} | {page_count}")
