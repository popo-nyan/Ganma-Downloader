import uuid
import httpx
from json import dumps

from .models import CreateAccountResponseBase, MagazineModel, MagazineItemBase


class Ganma:

    def __init__(self):
        self.__session = httpx.AsyncClient(http2=True, headers={
            'Host': 'reader.ganma.jp',
            'User-Agent': 'GanmaReader/9.0.0 Android releaseVersion:12 model:samsung/SC-51D',
            'X-From': 'https://reader.ganma.jp/api/',
            'X-Noescape': 'true',
            'Connection': 'close'})

    async def create_account(self) -> CreateAccountResponseBase | None:
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
                return CreateAccountResponseBase(user_id=data['id'],
                                                 password=data['password'])
        return None

    async def get_magazine_data(self,
                                magazine_alias: str
                                ) -> MagazineModel | None:
        response = await self.__session.get(url=f"https://reader.ganma.jp/api/3.2/magazines/{magazine_alias}")
        if response.status_code == httpx.codes.OK:
            response_json = response.json()['root']
            return MagazineModel(alias=response_json['alias'], author=response_json['author'],
                                 bookmarkCount=response_json['bookmarkCount'],
                                 canAcceptFanLetter=response_json['canAcceptFanLetter'],
                                 canSupport=response_json['canSupport'], description=response_json['description'],
                                 distributionLabel=response_json['distributionLabel'],
                                 firstViewAdvertisements=response_json['firstViewAdvertisements'],
                                 footerAdvertisements=response_json['footerAdvertisements'],
                                 heartCount=response_json['heartCount'],
                                 highlightImageURLs=response_json['highlightImageURLs'], id=response_json['id'],
                                 isGTOON=response_json['isGTOON'], isSeriesBind=response_json['isSeriesBind'],
                                 items=[MagazineItemBase(storyId=item['storyId'], title=item['title'],
                                                         seriesTitle=item['seriesTitle'],
                                                         thumbnailImageURL=item['thumbnailImageURL'], kind=item['kind'],
                                                         releaseStart=item['releaseStart'],
                                                         heartCount=item['heartCount'], disableCM=item['disableCM'],
                                                         hasExchange=item['hasExchange'])
                                        for item in response_json['items']], overview=response_json['overview'],
                                 publicLatestStoryNumber=response_json['publicLatestStoryNumber'],
                                 recommendations=response_json['recommendations'],
                                 rectangleWithLogoImageURL=response_json['rectangleWithLogoImageURL'],
                                 relatedLink=response_json['relatedLink'],
                                 storyReleaseStatus=response_json['storyReleaseStatus'], tags=response_json['tags'],
                                 title=response_json['title'], upcoming=response_json['upcoming'])
        else:
            return None

    async def get_magazine_story_reader(self,
                                        magazine_alias: str,
                                        story_id: str):
        response = await self.__session.get(url="https://ganma.jp/api/graphql",
                                            params={
                                                'operationName': 'MagazineStoryReaderQuery',
                                                'variables': dumps(
                                                    {'magazineIdOrAlias': magazine_alias, 'storyId': story_id,
                                                     'publicKey': None}),
                                                'extensions': dumps({'persistedQuery': {'version': 1,
                                                                                        'sha256Hash': '60dae270d44f863e2f485a7fffe83abb5a1d6e3c4fea394e048524ca81c64ca8'}})})
        if response.status_code == httpx.codes.OK:
            response_json = response.json()['root']
