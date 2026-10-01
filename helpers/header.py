# from curl_cffi import requests
import json
import base64
from pathlib import Path

root = Path(__file__).resolve().parent.parent
path = root / "Input" / "helper.json"


class Config:
    def __init__(self, path):
        self.path = path
        self.data = self.load()

    def load(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def get(self, key):
        return self.data.get(key)


class header:
    def __init__(self, session=None):
        self.session = session

    def cookies(self):
        for c in self.session.cookies.jar:
            print(c.name, "=", c.value)
        cookie_header = "; ".join(
            f"{c.name}={c.value}" for c in self.session.cookies.jar
        )
        # print(cookie_header)
        return cookie_header

    def context_prop(self, guild_id, channel_id, channel_type):
        context_properties = {
            "location": "Join Guild",  # other location require   like message id etc depending on which location value you are using
            "location_guild_id": guild_id,
            "location_channel_id": channel_id,
            "location_channel_type": channel_type,
        }
        data = json.dumps(context_properties, separators=(",", ":"))

        return base64.b64encode(data.encode("utf-8")).decode("utf-8")

    def installation_id(self):
        r = self.session.get("https://discord.com/api/v10/apex/experiments?surface=2")
        data = r.json()
        install_id = data.get("installation")
        if install_id:
            return install_id
        else:
            return "1539020270457725038.hs9HagILfzvLTvfr_YgmZCndCvc"
