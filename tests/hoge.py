import pprint
import httpx

from json import dumps

headers = {
    'Host': 'ganma.jp',
    'Accept': 'application/json',
    'User-Agent': 'GanmaReader/9.0.0 Android releaseVersion:12 model:samsung/SM-N976N',
    'X-From': 'https://reader.ganma.jp/api/',
    'X-Noescape': 'true',
}

params = {
    'operationName': 'MagazineStoryReaderQuery',
    'variables': dumps(
        {'magazineIdOrAlias': 'eceb4210-35be-11e9-994b-06e4e79605e7', 'storyId': 'f0c691f0-38a7-11e9-994b-06e4e79605e7',
         'publicKey': None}),
    'extensions': dumps({'persistedQuery': {'version': 1,
                                            'sha256Hash': '60dae270d44f863e2f485a7fffe83abb5a1d6e3c4fea394e048524ca81c64ca8'}}),
}

response = httpx.get('https://ganma.jp/api/graphql', params=params, headers=headers)
pprint.pprint(response.json())
