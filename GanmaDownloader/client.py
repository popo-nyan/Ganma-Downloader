import uuid
import httpx
from string import punctuation
from json import dumps
import aiofiles

from .models import CreateAccountResponseModel, MagazineResponseModel, MagazineItemBaseModel, \
    MagazineStoryReaderResponseModel, PageImageBaseModel, StoryInfoBaseModel, StoryContentBaseModel, \
    SearchComicResponseBaseModel, ApolloOperation
from .utils import make_directory


class Client:

    def __init__(self):
        self._app_version = "9.2.0"
        self._api_headers = {'Host': 'reader.ganma.jp',
                             'User-Agent': f'GanmaReader/{self._app_version} Android releaseVersion:12 model:samsung/SC-51D',
                             'X-From': 'https://reader.ganma.jp/api/',
                             'X-Noescape': 'true',
                             'Connection': 'close'}
        self._reder_headers = {'Host': 'ganma.jp',
                               'X-Apollo-Operation-Id': None,
                               'X-Apollo-Operation-Name': None,
                               'Accept': 'multipart/mixed; deferSpec=20220824, application/json',
                               'User-Agent': f'GanmaReader/{self._app_version} Android releaseVersion:9 model:samsung/SM-G973N',
                               'X-From': 'https://reader.ganma.jp/api/',
                               'X-Noescape': 'true'}
        self.__session = httpx.AsyncClient(http2=True)
        self._play_session = ""

    async def create_account(self) -> CreateAccountResponseModel | None:
        create_account_response = await self.__session.post(url="https://reader.ganma.jp/api/1.0/account",
                                                            headers=self._api_headers)
        if create_account_response.status_code == httpx.codes.OK:

            data = {"id": create_account_response.json()['root']['id'],
                    "password": create_account_response.json()['root']['password']}

            login_response = await self.__session.post(url="https://reader.ganma.jp/api/3.0/session",
                                                       headers=self._api_headers,
                                                       params={'clientType': 'app',
                                                               'installationId': str(uuid.uuid4()),
                                                               'explicit': 'false'},
                                                       data=data)
            if login_response.status_code == httpx.codes.OK and login_response.json()['success']:
                self._play_session = login_response.cookies.get("PLAY_SESSION")
                return CreateAccountResponseModel(user_id=data['id'],
                                                  password=data['password'])
        return None

    async def get_magazine_data(self,
                                magazine_alias: str
                                ) -> MagazineResponseModel | None:
        response = await self.__session.get(url=f"https://reader.ganma.jp/api/3.2/magazines/{magazine_alias}",
                                            headers=self._api_headers)
        if response.status_code == httpx.codes.OK:
            response_json = response.json()['root']
            stories = []
            for story in response_json['items']:
                if story.get("subtitle") is None:
                    continue
                stories.append(MagazineItemBaseModel(storyId=story['storyId'],
                                                     title=story['title'],
                                                     seriesTitle=story['seriesTitle'],
                                                     subtitle=story['subtitle'],
                                                     thumbnailImageUrl=story['thumbnailImageURL'],
                                                     kind=story['kind'],
                                                     releaseStart=story['releaseStart'],
                                                     heartCount=story['heartCount'],
                                                     disableCm=story['disableCM']))

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
        self._reder_headers['X-Apollo-Operation-Id'] = ApolloOperation.MagazineStoryReaderQuery.value
        self._reder_headers['X-Apollo-Operation-Name'] = ApolloOperation.MagazineStoryReaderQuery.name

        response = await self.__session.get(url="https://ganma.jp/api/graphql",
                                            headers=self._reder_headers,
                                            params={'operationName': 'MagazineStoryReaderQuery',
                                                    'variables': dumps({'magazineIdOrAlias': magazine_alias,
                                                                        'storyId': story_id,
                                                                        'publicKey': None}),
                                                    'extensions': dumps({'persistedQuery': {'version': 1,
                                                                                            'sha256Hash': ApolloOperation.MagazineStoryReaderQuery.value}})})
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
                                   subtitle: str) -> bool:
        save_image_path = (alias.strip(r"\\" + punctuation) + r"\\" +
                           title.strip(r"\\" + punctuation) + "-" +
                           subtitle.strip(r"\\" + punctuation))
        make_directory(alias.strip(r"\\" + punctuation))
        make_directory(save_image_path)
        response = await self.__session.get(url=base_url + str(page_count) + ".jpg?" + image_sign,
                                            headers={'Host': 'd1bzi54d5ruxfk.cloudfront.net',
                                                     'Accept-Encoding': 'gzip, deflate, br',
                                                     'User-Agent': f'GanmaReader/{self._app_version} Android releaseVersion:12 model:samsung/SC-51D'})
        if response.status_code == httpx.codes.OK:
            async with aiofiles.open(save_image_path + r"\\" + str(page_count) + ".jpg", "wb") as f:
                await f.write(response.content)
            print(f"[INFO] Success download image | {alias} | {title} | {subtitle} | {page_count}")
            return True
        else:
            print(f"[ERROR] The image could not be downloaded | {alias} | {title} | {subtitle} | {page_count}")
            return False

    async def search_magazine(self,
                              keyword: str) -> list[SearchComicResponseBaseModel] | None:
        self._reder_headers['X-Apollo-Operation-Id'] = ApolloOperation.SearchComic.value
        self._reder_headers['X-Apollo-Operation-Name'] = ApolloOperation.SearchComic.name

        response = await self.__session.get('https://ganma.jp/api/graphql',
                                            params={
                                                'operationName': 'SearchComic',
                                                'variables': dumps({'query': keyword, 'first': 50, 'after': None}),
                                                'extensions': dumps({'persistedQuery': {'version': 1,
                                                                                        'sha256Hash': ApolloOperation.SearchComic.value}})},
                                            headers=self._reder_headers)
        if response.status_code == httpx.codes.OK:
            response_json = response.json()
            magazines = []
            for magazine in response_json['data']['searchComic']['edges']:
                if magazine['node']['__typename'] != "Magazine":
                    continue
                magazines.append(SearchComicResponseBaseModel(type_name=magazine['node']['__typename'],
                                                              title=magazine['node']['title'],
                                                              magazine_id=magazine['node']['magazineId'],
                                                              todays_jacket_image_url=magazine['node']
                                                              ['todaysJacketImageURL'],
                                                              author_name=magazine['node']['authorName']))
            return magazines
        else:
            return None
