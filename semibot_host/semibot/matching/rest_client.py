import requests
from django.conf import settings

##
## REST API操作プログラム
##
## settings.pyにMATCHING_REST_URL_ROOTを指定する

## 外部モデルクラス
## data: 生データ、list型
## TODO: Pandasを利用するなどして相互変換(使いやすい形<-->json)やる
class RemoteModel:
    def __init__(self, url):
        self.response = requests.get(url)
        self.data = self.response.json()