# ;-;
from helpers.header import Config
from helpers.sup_prop import ua_builder
from pathlib import Path
from helpers.log import *

root = Path(__file__).resolve().parent.parent
path = root / "Input" / "helper.json"


def get_code():
    code = inputt("Input invite code: ")
    return code


def get_info(
    code, session, token, ua, sec_ch_ua, sec_ch_ua_platform, sup_prop, installation_id
):

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://discord.com/channels/1537426556165554216/1537429327719964716",
        "sec-ch-ua": sec_ch_ua,
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": sec_ch_ua_platform,
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": ua,
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "en-US",
        "x-discord-timezone": "Asia/Karachi",
        "x-installation-id": installation_id,
        "x-super-properties": sup_prop,
    }
    params = (
        ("inputValue", code),
        ("with_counts", "true"),
        ("with_expiration", "true"),
        ("with_permissions", "true"),
    )

    response = session.get(
        f"https://discord.com/api/v9/invites/{code}", headers=headers, params=params
    )
    r_json = response.json()
    if response.status_code == 200:
        guild_id = r_json["guild_id"]
        channel_id = r_json["channel"]["id"]
        channel_type = r_json["channel"]["type"]
        return guild_id, channel_id, channel_type

    error(f"get_info failed: {response.status_code}")
    print(response.text)
    return None
