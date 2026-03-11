import os
import time
from typing import Any, Dict, Optional

import requests


class GitHubGraphQLClient:
    def __init__(self, token: Optional[str] = None) -> None:
        self._token = token or os.getenv("GITHUB_TOKEN")
        if not self._token:
            raise ValueError("GITHUB_TOKEN environment variable is required")

        self._url = "https://api.github.com/graphql"
        self._headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github+json",
        }

    def execute(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        max_retries: int = 5,
    ) -> Dict[str, Any]:
        payload = {
            "query": query,
            "variables": variables or {},
        }

        for attempt in range(max_retries):
            response = requests.post(
                self._url,
                json=payload,
                headers=self._headers,
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()

                if "errors" in data:
                    raise RuntimeError(f"GraphQL errors: {data['errors']}")

                return data

            if response.status_code in (429, 502, 503, 504):
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue

            raise RuntimeError(
                f"GitHub API request failed with status {response.status_code}: {response.text}"
            )

        raise RuntimeError("GitHub API request failed after retries")