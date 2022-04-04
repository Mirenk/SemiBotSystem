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
    def __init__(self, send_dm=False, debug=False):
        self.debug = debug
        if send_dm:
            try:
                self.client = slack.WebClient(token=os.environ.get('SLACK_API_TOKEN'))
            except Exception:
                self.client = None
        else:
            self.client = None

    def __post_msg(self, channel, msg):
        try:
            res = self.client.chat_postMessage(channel=channel, text=msg)
        except SlackApiError as e:
            print(f"__post_msg: {e.res['error']}")

    def send_dm(self, userid: str, msg: str):
        if self.debug or self.client is None:
            print('SlackAPI: userid: ', userid)
            print('SlackAPI: msg: ', msg)

        if self.client is not None:
            try:
                res = self.client.conversations_open(users=userid)
            except SlackApiError as e:
                print(f"send_dm: {e.response['error']}")
                return
            else:
                dm_channel = res["channel"]["id"]
                self.__post_msg(dm_channel, msg)