import pprint

import httpx

cookies = {
    'PLAY_SESSION': 'eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7IlgtR2FubWEtUmVhZGVyLVNlc3Npb24iOiJpZD1jMWMyYWQ2MC1kZmMwLTExZWUtODc0My0zZTg5YzQ0OWRmNTA6dGltZXN0YW1wPTE3MTAxODAzOTIwMDAifSwiZXhwIjoxNzExMzg5OTkyLCJuYmYiOjE3MTAxODAzOTIsImlhdCI6MTcxMDE4MDM5Mn0.Ep_OqNAAJ6mhJJ2_BxmKaLWOEGlBKuNdl4R1tpLB3pY',
}

headers = {
    'Host': 'ganma.jp',
    'X-Apollo-Operation-Id': '60dae270d44f863e2f485a7fffe83abb5a1d6e3c4fea394e048524ca81c64ca8',
    'X-Apollo-Operation-Name': 'MagazineStoryReaderQuery',
    'Accept': 'multipart/mixed; deferSpec=20220824, application/json',
    'User-Agent': 'GanmaReader/9.0.0 Android releaseVersion:12 model:samsung/SM-N976N',
    'X-From': 'https://reader.ganma.jp/api/',
    'X-Noescape': 'true',
}

params = {
    'operationName': 'MagazineStoryReaderQuery',
    'variables': '{"magazineIdOrAlias": "eceb4210-35be-11e9-994b-06e4e79605e7", "storyId": "279dabe0-3322-11e9-994b-06e4e79605e7", "publicKey": "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALLsSK70DMZyR2Fn3rOKyyjmYQsR6ajPdE6++H7NQdY98g9tBXd0lXPNPfIGI5Y5vPHtUwjINxazjgrzGaXY97cCAwEAAQ=="}',
    'extensions': '{"persistedQuery": {"version": 1, "sha256Hash": "60dae270d44f863e2f485a7fffe83abb5a1d6e3c4fea394e048524ca81c64ca8"}}'
}

response = httpx.get('https://ganma.jp/api/graphql', params=params, cookies=cookies, headers=headers)
pprint.pprint(response.json())
