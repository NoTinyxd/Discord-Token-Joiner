# more stuff then sup_properties, includes other header stuffs as well


import re
from helpers.session import get_session
import random
import uuid
import json
import base64


class ua_builder:
    def __init__(self, ua, session=None):
        self.ua = ua
        self.session = session if session is not None else get_session()

    def version(self):
        match = re.search(r"Chrome/(\d+)", self.ua)
        if match:
            chrome_version = match.group(1)
            return chrome_version
        else:
            return "The ua value is empty"

    def greese_builder(self):

        brands = [
            "Not(A:Brand",
            "Not A;Brand",
            "Not A Brand",
            "Not/A)Brand",
            "Not-A?Brand",
            "Not A.Brand",
        ]
        versions = ["8", "99"]
        if not hasattr(self, "_greese"):
            self._greese = (random.choice(brands), random.choice(versions))
        return self._greese

    def sec_ch_ua(self):
        greese_brand, greese_version = self.greese_builder()
        version = self.version()
        brands = [
            (greese_brand, greese_version),
            ("Chromium", version),
            ("Google Chrome", version),
        ]
        random.shuffle(brands)
        return ", ".join(f'"{b}";v="{v}"' for b, v in brands)

    def sec_ch_ua_platform(self):
        ua = self.ua

        if "Windows" in ua:
            return "Windows"
        elif "Mac OS X" in ua:
            return "macOS"
        elif "Linux" in ua and "Android" not in ua:
            return "Linux"
        elif "Android" in ua:
            return "Android"
        elif "iPhone" in ua or "iPad" in ua:
            return "iOS"
        else:
            return "see your useragent"

    def get_browser(self):
        ua = self.ua
        if "OPR/" in ua or "Opera" in ua:
            return "Opera"
        elif "Chrome/" in ua and "Chromium/" not in ua:
            return "Chrome"
        elif "Firefox/" in ua:
            return "Firefox"
        elif "Safari/" in ua and "Chrome/" not in ua:
            return "Safari"
        else:
            return "add urself"

    def builder_id(self):
        r = self.session.get("https://discord.com")
        match = re.search(r'"BUILD_NUMBER":"(\d+)"', r.text)

        if match:
            build_number = int(match.group(1))
            return build_number
        else:
            return "594031"

    def sup_prop(self):
        launch_id = str(uuid.uuid4())
        launch_signature = str(uuid.uuid4())
        heartbeat_id = str(uuid.uuid4())
        REFERRERS = [
            ("https://www.google.com/", "www.google.com"),
            ("https://www.google.co.uk/", "www.google.co.uk"),
            ("https://www.bing.com/", "www.bing.com"),
            ("https://search.brave.com/", "search.brave.com"),
            ("https://search.yahoo.com/", "search.yahoo.com"),
        ]
        referrer, referring_domain = random.choice(REFERRERS)
        sup_prop = {
            "os": self.sec_ch_ua_platform(),
            "browser": self.get_browser(),
            "device": "",
            "system_locale": "en-US",
            "has_client_mods": False,
            "browser_user_agent": self.ua,
            "browser_version": self.version(),
            "os_version": "",
            "referrer": referrer,
            "referring_domain": referring_domain,
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": self.builder_id(),
            "client_event_source": None,
            "client_launch_id": launch_id,
            "launch_signature": launch_signature,
            "client_heartbeat_session_id": heartbeat_id,
            "client_app_state": "focused",
        }
        saparators = (",", ":")
        d = json.dumps(sup_prop, separators=saparators)
        return base64.b64encode(d.encode()).decode()
