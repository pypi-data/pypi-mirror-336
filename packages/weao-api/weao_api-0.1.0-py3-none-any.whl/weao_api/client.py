import requests
import urllib.parse

from .exceptions import WEAOAPIError

class WEAOAPIClient:
    """
    Client for interacting with the WEAO API.
    """
    BASE_URL = "https://weao.xyz/api"
    HEADERS = {"User-Agent": "WEAO-3PService"}

    def __init__(self, timeout: int = 10):
        """
        Initialize the client.
        
        :param timeout: Request timeout in seconds (default is 10).
        """
        self.timeout = timeout

    def _get(self, endpoint: str):
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, headers=self.HEADERS, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise WEAOAPIError(f"GET request failed: {e}")

    def _post(self, endpoint: str, payload: dict):
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.post(url, json=payload, headers=self.HEADERS, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise WEAOAPIError(f"POST request failed: {e}")

    def get_current_versions(self) -> dict:
        """
        Retrieve the current Roblox versions for Windows and Mac.
        """
        return self._get("/versions/current")

    def get_future_versions(self) -> dict:
        """
        Retrieve the future Roblox versions for Windows and Mac.
        """
        return self._get("/versions/future")

    def get_android_version(self) -> dict:
        """
        Retrieve the current Roblox version for Android.
        """
        return self._get("/versions/android")

    def get_all_exploits(self) -> list:
        """
        Retrieve the statuses of all exploits.
        """
        return self._get("/status/exploits")

    def get_exploit_status(self, exploit: str) -> dict:
        """
        Retrieve the status for a specific exploit.

        :param exploit: The name or identifier of the exploit.
        """
        encoded_exploit = urllib.parse.quote(exploit)
        return self._get(f"/status/exploits/{encoded_exploit}")

    def get_api_health(self) -> dict:
        """
        Retrieve the health status of the WEAO API.
        """
        return self._get("/health")

    def update_exploit(
        self, 
        api_key: str, 
        updated: bool, 
        version: str, 
        feature: bool = False, 
        ping: bool = False, 
        changelog: str = ""
    ) -> dict:
        """
        Update the status of an exploit via the API.
        
        :param api_key: Your exploit API key.
        :param updated: Boolean indicating if the exploit is updated.
        :param version: The version of your exploit.
        :param feature: True if this is a feature update (default: False).
        :param ping: Set to False to avoid pinging the Discord server (default: False).
        :param changelog: Optional changelog information.
        :return: API response as a dictionary.
        """
        payload = {
            "apiKey": api_key,
            "updated": updated,
            "version": version,
            "feature": feature,
            "ping": ping,
            "changelog": changelog
        }
        return self._post("/status/update", payload)
