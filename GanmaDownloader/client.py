import pprint
import uuid
import httpx

from typing import Optional
from .models import CreateAccountResponseBase, MagazineModel


class Ganma:
    
    def __init__(self):
        self.__session = httpx.AsyncClient(http2=True, headers={
            "Host": "reader.ganma.jp",
            "User-Agent": "GanmaReader/9.0.0 Android releaseVersion:12 model:samsung/SC-51D",
            "X-From": "https://reader.ganma.jp/api/",
            "X-Noescape": "true",
            "Connection": "close"})
    
    async def create_account(self) -> Optional[CreateAccountResponseBase]:
        create_account_response = await self.__session.post(url="https://reader.ganma.jp/api/1.0/account")
        if create_account_response.status_code == httpx.codes.OK:
            params = {
                "clientType": "app",
                "installationId": str(uuid.uuid4()),
                "explicit": "false"}
            data = {"id": create_account_response.json()["root"]["id"],
                    "password": create_account_response.json()["root"]["password"]}
            login_response = await self.__session.post(url="https://reader.ganma.jp/api/3.0/session",
                                                       params=params,
                                                       data=data)
            if login_response.status_code == httpx.codes.OK and login_response.json()["success"]:
                return CreateAccountResponseBase.model_validate(create_account_response.json()["root"])
        return None
    
    async def get_magazine_data(self,
                                magazine_alias: str
                                ) -> Optional[MagazineModel]:
        response = await self.__session.get(url=f"https://reader.ganma.jp/api/3.2/magazines/{magazine_alias}")
        if response.status_code == httpx.codes.OK:
            return MagazineModel.model_validate(response.json()["root"])
        else:
            return None
