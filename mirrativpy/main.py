# Copyright (c) 2020 Ch31212y
# Released under the MIT license
# https://github.com/Ch31212y/mirrativpy/blob/master/LICENSE

import requests
from .config import Config
import json
from random import choice


class Mirrativ:
    def __init__(self):
        self.session = requests.Session()
        headers = {"User-Agent": Config.USER_AGENT}
        self.session.headers = headers

    def get_user_id(self) -> str:
        req = self.session.get(
            Config.HOST_URL + Config.USER_ME
        )
        self.session.cookies = req.cookies
        reqjs = req.json()
        self.user_id = reqjs["user_id"]
        self.usernames = reqjs["capabilities"]["default_names"]
        return self.user_id

    def create_account(self, name=None, random=False):
        id_ = self.get_user_id()
        if random is True:
            self.name = choice(self.usernames)
        else:
            self.name = name
        body = dict(
            user_id=id_,
            name=self.name,
            include_urge_users=1,
            dynamic_ling=""
        )
        req = self.session.post(
            Config.HOST_URL + Config.PROFILE_EDIT,
            data=body
        )
        if req.status_code == 200:
            return print("success create account")
        raise Exception(f"Failed with status_code {req.status_code}")

    def follow(self, target_userid: str):
        body = {"user_id": target_userid}
        req = self.session.post(
            Config.HOST_URL + Config.FOLLOW,
            data=body
        )
        if req.status_code == 200:
            return print(f"success follow user : {target_userid}")
        raise Exception(f"Failed with status_code {req.status_code}")

    def comment_on_live(self, live_id: str, comment: str):
        body = {
            "live_id": live_id,
            "comment": comment,
            "type": "1",
            "where": "template_comment"
        }
        req = self.session.post(
            Config.HOST_URL + Config.COMMENT,
            data=body
        )
        if req.status_code == 200:
            return print(f"success create comment on live id : {live_id}")
        raise Exception(f"Failed with status_code {req.status_code}")

    def join_live(self, live_id: str):
        # 参加通知がこない
        req = self.session.get(
            Config.HOST_URL + Config.LIVE,
            params={"live_id": live_id}
        )
        if req.status_code == 200:
            return print("ok")
        raise Exception(f"Failed with status_code {req.status_code}")

    def stay_arrive_live(self, live_id: str) -> int:
        data = {
            "live_id": live_id,
            "live_user_key": "",
            "is_ui_hidden": "0"
        }
        req = self.session.post(
            Config.HOST_URL + Config.LIVE_POLLING,
            data=data
        )
        if req.status_code == 200:
            return req.json()["total_viewer_num"]
        raise Exception(f"Failed with status_code {req.status_code}")

    def live_requests(self, user_id: str, count: int):
        data = {
            "user_id": user_id,
            "count": str(count),
            "where": "live_view_end"
        }
        req = self.session.post(
            Config.HOST_URL + Config.LIVE_REQUESTS,
            data=data
        )
        if req.status_code == 200:
            return print("ok")
        raise Exception(f"Failed with status_code {req.status_code}")

    def get_comment(self, live_id: str) -> []:
        req = self.session.get(
            Config.HOST_URL + Config.GET_COMMENT,
            params={"live_id": live_id}
        )
        rej = req.json()
        return [x["comment"] for x in rej["comments"]]

    def get_streaming_url(self, live_id: str):
        req = self.session.get(
            Config.HOST_URL + Config.STREAM_URL,
            params={"live_id": live_id}
        )
        if req.status_code == 200:
            return print("ok")
        raise Exception(f"Failed with status_code {req.status_code}")

    def get_live_id(self) -> str:
        req = self.session.post(
            Config.HOST_URL + Config.CREATE_LIVE,
            data={"is_private": "1"}
        )
        return req.json()["live_id"]

    def start_live(self):
        data = {
            "live_id": self.get_live_id(),
            "title": "てすと配信",
            "description": "",
            "orientation": "1",
            "orientation_v2": "1",
            "collab_enabled": "1",
            "max_collab_user_num": "3"
        }
        req = self.session.post(
            Config.HOST_URL + Config.EDIT_LIVE,
            data=data
        )
        return req.json()["shares"]["others"]["text"]
