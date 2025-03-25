import requests
from typing import Optional, Dict, Any

class TRWClient:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the TRW API client
        
        Args:
            api_key (str, optional): Your TRW API key. Not required for free endpoints.
        """
        self.api_key = api_key
        self.base_url = "https://iwoozie.baby/api"
        self.headers = {
            "Content-Type": "application/json"
        }
        if api_key:
            self.headers["x-api-key"] = api_key

    def _make_request(self, method: str, endpoint: str, params: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Internal method to make API requests
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()

    def bypass(self, url: str) -> Dict[str, Any]:
        """
        Performs a general bypass
        
        Args:
            url (str): URL to process
            
        Returns:
            dict: Bypass result
        """
        return self._make_request("GET", "bypass", params={"url": url})

    def bypass_v2(self, url: str) -> Dict[str, Any]:
        """
        Initiates a long-duration bypass
        
        Args:
            url (str): URL to process
            
        Returns:
            dict: Information about the initiated thread
        """
        return self._make_request("GET", "v2/bypass", params={"url": url})

    def check_thread(self, thread_id: str) -> Dict[str, Any]:
        """
        Checks the status of a long-duration bypass
        
        Args:
            thread_id (str): ID of the thread to check
            
        Returns:
            dict: Current bypass status
        """
        return self._make_request("GET", "v2/threadcheck", params={"id": thread_id})

    def get_status(self) -> Dict[str, Any]:
        """
        Gets the API status
        
        Returns:
            dict: Current API status
        """
        return self._make_request("GET", "status")

    def free_bypass(self, url: str) -> Dict[str, Any]:
        """
        Performs a bypass using the free endpoint
        
        Args:
            url (str): URL to process
            
        Returns:
            dict: Bypass result
        """
        return self._make_request("GET", "free/bypass", params={"url": url})
