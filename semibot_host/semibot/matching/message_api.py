from abc import ABCMeta, abstractmethod
import slack
from slack.errors import SlackApiError
import os

# 基底メッセージAPIクラス
# これを継承して他のメッセージサービスに対応させる
class BaseMessageAPI(metaclass=ABCMeta):
    @abstractmethod
    def send_dm(self, userid: str, msg: str):
        pass

class SlackAPI(BaseMessageAPI):
    def __init__(self):
        self.client = slack.WebClient(token=os.environ.get('SLACK_API_TOKEN'))

    def __post_msg(self, channel, msg):
        try:
            res = self.client.chat_postMessage(channel=channel, text=msg)
            assert res["message"]["text"] == msg
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"__post_msg: {e.res['error']}")

    def send_dm(self, userid: str, msg: str):
        try:
            res = self.client.conversations_open(users=userid)
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"send_dm: {e.response['error']}")
            return
        else:
            dm_channel = res["channel"]["id"]
            self.__post_msg(dm_channel, msg)

    # デバッグ用
    def print_send_dm(self, userid: str, msg: str):
        print('SlackAPI: userid: ', userid)
        print('SlackAPI: msg: ', msg)