import uuid
import httpx
import pprint
from json import dumps

from .models import CreateAccountResponseModel, MagazineResponseModel, MagazineItemBaseModel
from .utils import make_directory

class Ganma:

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
                                         items=[MagazineItemBaseModel(story_id=item['storyId'],
                                                                      title=item['title'],
                                                                      series_title=item['seriesTitle'],
                                                                      thumbnail_image_url=item['thumbnailImageURL'],
                                                                      kind=item['kind'],
                                                                      release_start=item['releaseStart'],
                                                                      heart_count=item['heartCount'],
                                                                      disable_cm=item['disableCM'],
                                                                      has_exchange=item['hasExchange'])
                                                for item in response_json['items']],
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
                                        story_id: str):
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
        print(response.url)
        if response.status_code == httpx.codes.OK:
            pprint.pprint(response.json())
