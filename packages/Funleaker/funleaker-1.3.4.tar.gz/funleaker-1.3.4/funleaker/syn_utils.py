import os
import requests
import json
import time
from urllib.parse import urlparse
from datetime import datetime, timedelta
from tqdm import tqdm
from colorama import Fore, Style, init as colorama_init
import xml.etree.ElementTree as ET

colorama_init(autoreset=True)
"""
syn_utils is a utility class to interact with the Syn API service. It handles user login, token management,
rate-limiting, leaks management, and logging functionality.

It provides methods for logging into the service, verifying tokens, and performing leaks across platforms.
"""
class syn_utils:
    """
    Initializes the syn_utils class, setting up necessary configurations, token cache, and rate-limiting settings.

    Attributes:
    - lowLvlLog (bool): Controls whether to show lower-level log messages (default is True).
    - showProgressBar (bool): Controls whether to show a progress bar for operations (default is True).
    """
    def __init__(self, lowLvlLog=True, showProgressBar=True):
        self.lowLvlLog = lowLvlLog
        self.showProgressBar = showProgressBar

        # Initialize other attributes as before
        self._api_config = None
        self._access_key = None
        self._uid = None
        self._user_data = None
        self._current_version = None
        self._intlized = False
        self._last_request_time = None
        self._rate_limit = 1
        self._token_cache_file = "token_cache.json"

        # Load cached token if available
        self._load_cached_token()

        # Print the initial message based on the `lowLvlLog` flag
        if self.lowLvlLog:
            self._print_info("Initializing the tool...")

    def _print_error(self, msg):
        """ Prints an error message to the console with a red color indicator. """
        print(Fore.RED + "[ERROR] " + msg)

    def _print_success(self, msg):
        """ Prints a success message to the console with a green color indicator. """
        print(Fore.GREEN + "[SUCCESS] " + msg)

    def _print_info(self, msg):
        """ Prints an informational message to the console with a cyan color indicator. """
        print(Fore.CYAN + "[INFO] " + msg)

    def _load_cached_token(self):
        """ Loads the cached token (if available) from the token cache file. """
        if os.path.exists(self._token_cache_file):
            with open(self._token_cache_file, "r") as f:
                cached_data = json.load(f)
                self._uid = cached_data.get("uid")
                self._access_key = cached_data.get("access_key")

    def _save_cached_token(self):
        """ Saves the current token to a local cache file for reuse in future sessions. """
        if self._uid and self._access_key:
            with open(self._token_cache_file, "w") as f:
                json.dump({"uid": self._uid, "access_key": self._access_key}, f)

    def _clear_cached_token(self):
        """ Clears the cached token and UID stored in the token cache file. """
        if os.path.exists(self._token_cache_file):
            os.remove(self._token_cache_file)
            self._uid = None
            self._access_key = None
            if self.lowLvlLog:
                self._print_success("Successfully logged out and cleared the cached token.")

    """ Logs the user out by clearing the cached token and UID. """
    def logout(self):
        self._clear_cached_token()
        if self.lowLvlLog:
            self._print_success("Logged out successfully.")

    def _rate_limit_check(self):
        """ Checks if the rate-limiting condition has been met. """
        current_time = datetime.now()
        if self._last_request_time and current_time - self._last_request_time < timedelta(seconds=1 / self._rate_limit):
            self._print_error("Rate limit exceeded. Please try again later.")
            return False
        self._last_request_time = current_time
        return True

    def intlize(self):
        """ Initializes the Syn service by making an API call to fetch configuration data. """
        if self.lowLvlLog:
            self._print_info("Initializing the tool...")

        try:
            res = requests.get("https://api.jsonsilo.com/public/1120b51d-8965-4023-aae4-64e4402c708a")
            res.raise_for_status()
            data = res.json()

            funleaker_data = data.get("FunLeakerPypi", {})
            if not funleaker_data.get("EnableLogin", False):
                self._print_error(f"This version of syn service ({funleaker_data.get('AppVholder')}) is disabled.")
                return False

            if not data.get("extension", {}).get("EnableLogin", False):
                self._print_error("Login to Syn account is disabled.")
                return False

            self._api_config = funleaker_data["api_config"]
            self._current_version = funleaker_data["CurrentVersion"]
            self._intlized = True

            if self.lowLvlLog:
                self._print_success("Tool initialized successfully.")
            return True

        except Exception as e:
            self._print_error("Something went wrong in the tool configurations.")
            return False

    def login(self, username, password, saveTokenInDevice=False):
        """ Logs the user into the Syn service using their username and password. """
        if not self._intlized:
            self.intlize()

        if self._uid and self._access_key:  # Check if already logged in
            if self.lowLvlLog:
                self._print_success("Already logged in.")
            return True

        if self.lowLvlLog:
            self._print_info("Attempting to log in...")

        try:
            url = f"{self._api_config}login.php"
            payload = {
                'username': username,
                'password': password,
                'source': self._current_version,
            }
            headers = {
                'X_SYN_ACCESS': 'AA1DEV4T-84544ZZ51784-EFEA15',
            }

            # Add progress bar during login if showProgressBar is True
            if self.showProgressBar:
                for _ in tqdm(range(10), desc="Logging in..."):
                    time.sleep(0.05)

            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            data = response.json()

            if not data.get("status"):
                self._print_error("Login failed: " + data.get("msg", "Invalid username or password."))
                return False

            self._access_key = data["data"]
            self._uid = data["puid"]
            self._user_data = data

            if saveTokenInDevice:
                self._save_cached_token()  # Cache token for future use

            if self.lowLvlLog:
                self._print_success("Successfully logged in to Syn account.")
            return True

        except Exception:
            self._print_error("Failed to login to Syn account.")
            return False

    def _verify_token(self):
        """ Verifies the token for login and access to the Syn service. """
        if self.lowLvlLog:
            self._print_info("Verifying access token...")

        try:
            verify_url = f"{self._api_config}verify_token.php"
            headers = {
                'X_SYN_ACCESS': 'AA1DEV4T-84544ZZ51784-EFEA15'
            }
            payload = {
                "access_key": self._access_key,
                "uid": self._uid
            }

            response = requests.post(verify_url, headers=headers, data=payload)
            data = response.json()

            if not data.get("status"):
                self._print_error("Failed to verify your access to the Syn account.")
                return False

            if self.lowLvlLog:
                self._print_success("Access token verified.")
            return True

        except Exception:
            self._print_error("Token verification failed.")
            return False
    """
    Performs a data leak operation on a given target URL (e.g., OnlyFans, Fansly, Patreon).
    
    This method searches for content related to the given target and can return the leak data in various formats.
    
    Parameters:
    - target (str): The URL or identifier of the creator.
    - login_method (str): The method to use for logging in ("login").
    - platform (str): The platform for which to perform the leak (e.g., "onlyfans", "fansly").
    - deepth (int): The number of pages to scrape (default is 0 for no depth).
    - LeakType (str): The type of leak (e.g., "VisualLeaks").
    - ReturnType (str): The format in which to return the results (e.g., "json", "text").
    - autoLeak (bool): Whether to automatically fetch all posts (default: True).

    Returns:
    - dict or str: The leak data in the specified format (e.g., JSON or text).
    """
    def DoLeak(self, target, login_method, platform=None, deepth=0, LeakType="VisualLeaks", ReturnType="json", autoLeak=True):

        if not self._uid or not self._access_key:
            self._print_error("You must login before performing any operations.")
            return

        if not self._verify_token():
            return

        if not self._rate_limit_check():  # Check rate limit before proceeding
            return

        parsed = urlparse(target)
        domain = parsed.netloc.lower()
        path = parsed.path.strip("/")
        username = path.split("/")[0] if path else None

        if "?" in username:
            username = username.split("?")[0]

        if not username:
            self._print_error("Invalid target URL: Cannot extract username.")
            return

        if domain not in ["onlyfans.com", "fansly.com", "patreon.com"]:
            self._print_error("Unsupported platform or invalid URL.")
            return

        platform = platform or domain.split(".")[0]
        host = "csyn" if platform in ["onlyfans", "fansly"] else "ksyn"
        source_domain = "coomer.su" if host == "csyn" else "kemono.su"

        self._print_info(f"Using source domain")
        url = f"https://{source_domain}/api/v1/creators.txt"

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                self._print_error(f"Failed to fetch creators.txt (Status: {response.status_code})")
                return

            creators = response.text.split("},{")
            matches = []
            target_name = username.lower().replace(" ", "")

            for i, raw in enumerate(tqdm(creators, desc="Searching for creators...")):
                if i == 0:
                    raw = "{" + raw
                elif i == len(creators) - 1:
                    raw = raw + "}"
                else:
                    raw = "{" + raw + "}"

                try:
                    data = json.loads(raw)
                    creator_name = data.get("name", "").lower().replace(" ", "")
                    creator_service = data.get("service", "").lower()

                    if creator_service != platform:
                        continue

                    # Use _levenshtein_distance to find similarity between target and creator name
                    score = self._levenshtein_distance(target_name, creator_name)

                    if score <= 3 or target_name in creator_name or creator_name in target_name:
                        matches.append({
                            "id": data.get("id"),
                            "name": data.get("name"),
                            "service": creator_service,
                            "indexed": data.get("indexed"),
                            "updated": data.get("updated"),
                            "favorited": data.get("favorited")
                        })

                        if len(matches) >= 4:
                            break

                except:
                    continue

            if not matches:
                self._print_error("No matching creators found.")
                return False

            self._print_success(f"Found {len(matches)} matched result(s):")
            for m in matches:
                print(f" - {m['name']} ({m['service']})")

            if not autoLeak:
                return self._format_output(matches, ReturnType)

            # AUTO LEAK MODE
            all_leaked_data = []
            for m in tqdm(matches, desc="Fetching leak data..."):
                user = m["name"]
                service = m["service"]

                offset = 0
                while True:
                    paged_url = f"https://{source_domain}/api/v1/{service}/user/{user}?o={offset}"
                    resp = requests.get(paged_url)
                    if resp.status_code != 200:
                        break

                    posts = resp.json()
                    if not posts:
                        break

                    for post in posts:
                        entry = {
                            "status": True,
                            "msg": "success",
                            "target_id": post.get("id"),
                            "target_name": post.get("user"),
                            "target_platform": post.get("service"),
                            "leakedPost_title": post.get("title"),
                            "leakedPost_content": post.get("content"),
                            "leakedPost_embed": post.get("embed", {}),
                            "leakedPost_IsSharedFile": post.get("shared_file"),
                            "LeakedPost_Created": post.get("added"),
                            "LeakedPost_Posted": post.get("published"),
                            "LeakedPost_EDIted": post.get("edited") or post.get("added"),
                            "leakedPost_Media": {
                                "source": post.get("file", {}).get("path"),
                                "source_name": post.get("file", {}).get("name")
                            },
                            "leakedPost_MediaAttachments": [
                                {
                                    "source": att.get("path"),
                                    "source_name": att.get("name")
                                } for att in post.get("attachments", [])
                            ],
                            "leakedPost_isPoll": post.get("poll"),
                            "leakedPost_captions": post.get("captions"),
                            "leakedPost_tags": post.get("tags")
                        }
                        all_leaked_data.append(entry)

                    offset += 50
                    if deepth and offset >= deepth:
                        break

            return self._format_output(all_leaked_data, ReturnType)

        except Exception as e:
            self._print_error("Internal server error during processing.")
            return False


    # Helper Methods

    def _levenshtein_distance(self, a, b):
        if len(a) < len(b):
            return self._levenshtein_distance(b, a)

        if len(b) == 0:
            return len(a)

        prev_row = list(range(len(b) + 1))
        for i, c1 in enumerate(a):
            curr_row = [i + 1]
            for j, c2 in enumerate(b):
                insertions = prev_row[j + 1] + 1
                deletions = curr_row[j] + 1
                substitutions = prev_row[j] + (c1 != c2)
                curr_row.append(min(insertions, deletions, substitutions))
            prev_row = curr_row

        return prev_row[-1]


    def _format_output(self, data, ReturnType):
        if ReturnType == "json":
            return data
        elif ReturnType == "text":
            return self._to_text(data)
        elif ReturnType == "html":
            return self._to_html(data)
        elif ReturnType == "xml":
            return self._to_xml(data)
        else:
            return data  # fallback to JSON

    def _to_text(self, data):
        out = []
        for item in data:
            block = "\n".join([f"{k}: {v}" for k, v in item.items()])
            out.append(block)
        return "\n\n---\n\n".join(out)

    def _to_html(self, data):
        html = "<html><body><h1>Leak Results</h1>"
        for item in data:
            html += "<div><ul>"
            for k, v in item.items():
                html += f"<li><strong>{k}:</strong> {v}</li>"
            html += "</ul></div><hr>"
        html += "</body></html>"
        return html

    def _to_xml(self, data):
        root = ET.Element("LeakResults")
        for item in data:
            entry = ET.SubElement(root, "Leak")
            for k, v in item.items():
                child = ET.SubElement(entry, k)
                child.text = json.dumps(v) if isinstance(v, (dict, list)) else str(v)
        return ET.tostring(root, encoding='unicode')
