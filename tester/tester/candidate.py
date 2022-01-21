import requests
import socket

# アンダーバーを含むドメインでDjangoはアクセスできないので、直引きして接続
HOST = "http://" + socket.gethostbyname("semibot_host") + ":8000"

# 候補者クラス
class Candidate:
    # オブジェクト生成時にログインを行う
    def __init__(self, username: str, password: str):
        login_url = HOST + "/login/"

        self.session = requests.session()
        self.session.get(login_url)
        csrf = self.session.cookies['csrftoken']

        data = {
            "csrfmiddlewaretoken": csrf,
            "username": username,
            "password": password,
        }

        self.session.post(login_url, data=data, headers=dict(Referer=login_url))

    # ページ取得
    def get(self, abs_url: str):
        return self.session.get(HOST + abs_url)