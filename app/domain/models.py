from dataclasses import dataclass


@dataclass(frozen=True)
class Repository:
    github_id: str
    repository_name: str
    owner_login: str
    repository_url: str
    stars_count: int