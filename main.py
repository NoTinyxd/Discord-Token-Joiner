from curl_cffi import requests
import json
from helpers.header import header
from helpers.sup_prop import *
import secrets
from helpers.session import *
from helpers.util import *
from helpers.log import *
from time import perf_counter
import os
import json
from pathlib import Path
from helpers.solver import *

root = Path(__file__).resolve().parent
helper_path = root / "Input" / "helper.json"


def terminal_clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


class Joiner:
    def __init__(self):
        self.code = get_code()
        self.url = f"https://discord.com/api/v9/invites/{self.code}"
        self.load_config()
        self.tokens = self.load_tokens()
        self.stars = "*" * 45  # just for masking the token
        self.path = helper_path

    def load_config(self):
        with helper_path.open("r") as f:
            d = json.load(f)
            ua = d.get("useragent")
            if isinstance(ua, list):
                self.uas = ua
            else:
                self.uas = [ua]

    def load_tokens(self):
        tokens = []
        tokens_path = root / "Input" / "tokens.txt"  # the file path containing tokens
        with tokens_path.open("r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(":")  # using : as seperator for s:s:token format
                if len(parts) == 3:
                    token = parts[2]
                elif len(parts) == 1:
                    token = parts[0]
                else:
                    continue

                tokens.append(token)
        return tokens

    def make_headers(self, token):
        return {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": token,
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": "https://discord.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://discord.com/channels/@me",
            "sec-ch-ua": self.sec_ch_ua,
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": self.sec_ch_ua_platform,
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.ua,
            "x-context-properties": self.context_properties,
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-discord-timezone": "Asia/Karachi",
            "x-installation-id": self.installation_id,
            "x-super-properties": self.sup_proper,
        }

    def join(self):
        terminal_clear()

        setup_session = get_session()
        setup_ua = self.uas[0]
        setup_u = ua_builder(setup_ua, setup_session)
        setup_sec_ch_ua = setup_u.sec_ch_ua()
        setup_sec_ch_ua_platform = setup_u.sec_ch_ua_platform()
        setup_sup_proper = setup_u.sup_prop()

        setup_h = header(setup_session)
        self.installation_id = setup_h.installation_id()

        info = get_info(
            self.code,
            setup_session,
            self.tokens[0],
            setup_ua,
            setup_sec_ch_ua,
            setup_sec_ch_ua_platform,
            setup_sup_proper,
            self.installation_id,
        )

        if not info:
            error("get_info failed")
            return

        (
            self.location_guild_id,
            self.location_channel_id,
            self.location_channel_type,
        ) = info

        self.context_properties = setup_h.context_prop(
            self.location_guild_id,
            self.location_channel_id,
            self.location_channel_type,
        )

        for i, token in enumerate(self.tokens):
            self.session = new_session()
            self.ua = self.uas[i % len(self.uas)]

            self.u = ua_builder(self.ua, self.session)
            self.sec_ch_ua = self.u.sec_ch_ua()
            self.sec_ch_ua_platform = self.u.sec_ch_ua_platform()
            self.sup_proper = self.u.sup_prop()

            self.cookie_dict = {c.name: c.value for c in self.session.cookies.jar}

            session_id = secrets.token_hex(16)
            headers = self.make_headers(token)
            data = json.dumps({"session_id": session_id})
            start = perf_counter()
            response = self.session.post(
                self.url, headers=headers, data=data, cookies=self.cookie_dict
            )
            took = f"{perf_counter() - start:.2f}s"

            if response.status_code == 200:
                success(
                    f"Joined {self.location_guild_id} | token={token[:29]}{self.stars}, res_code={response.status_code}, took={took}"
                )
            elif response.status_code == 400 and "captcha_key" in response.json():
                warning(
                    f"Failed {self.location_guild_id} | token={token[:29]}{self.stars}, res_code={response.status_code}, took={took}, reason=hcap"
                )

                print(response.json())
                captcha = response.json()

                sitekey = captcha.get("captcha_sitekey")
                rqdata = captcha.get("captcha_rqdata")
                rqtoken = captcha.get("captcha_rqtoken")
                session_id = captcha.get("captcha_session_id")
                solver = Solver("http://127.0.0.1:6465/solve")
                solvehcap = solver.solve(
                    sitekey=sitekey,
                    hostname="discord.com",
                    rqdata=rqdata,
                )

                headerss = self.make_headers(token)
                captcha_key = solvehcap.get("token")
                headerss.update(
                    {
                        "x-captcha-key": captcha_key,
                        "x-captcha-rqtoken": rqtoken,
                        "x-captcha-session-id": session_id,
                    }
                )
                again_response = self.session.post(
                    self.url, headers=headerss, data=data, cookies=self.cookie_dict
                )
                if again_response.status_code == 200:
                    success(
                        f"Joined {self.location_guild_id} | token={token[:29]}{self.stars}, res_code={response.status_code}, took={took},hcap_tok= {captcha_key[:40]}"
                    )
                else:
                    info(
                        f"res_code={again_response.status_code}, res={again_response.text}"
                    )

            else:
                print(response.text, response.status_code)


if __name__ == "__main__":
    joiner = Joiner()
    joiner.join()
