from typing import Iterable

from app.domain.models import Repository


UPSERT_REPOSITORY_SQL = """
INSERT INTO github_crawler.repositories (
    github_id,
    repository_name,
    owner_login,
    repository_url,
    stars_count,
    crawled_at,
    updated_at
)
VALUES (
    %(github_id)s,
    %(repository_name)s,
    %(owner_login)s,
    %(repository_url)s,
    %(stars_count)s,
    NOW(),
    NOW()
)
ON CONFLICT (github_id)
DO UPDATE SET
    repository_name = EXCLUDED.repository_name,
    owner_login = EXCLUDED.owner_login,
    repository_url = EXCLUDED.repository_url,
    stars_count = EXCLUDED.stars_count,
    crawled_at = NOW(),
    updated_at = NOW();
"""


def save_repositories(connection, repositories: Iterable[Repository]) -> None:
    rows = [
        {
            "github_id": repo.github_id,
            "repository_name": repo.repository_name,
            "owner_login": repo.owner_login,
            "repository_url": repo.repository_url,
            "stars_count": repo.stars_count,
        }
        for repo in repositories
    ]

    if not rows:
        return

    with connection.cursor() as cursor:
        cursor.executemany(UPSERT_REPOSITORY_SQL, rows)

    connection.commit()