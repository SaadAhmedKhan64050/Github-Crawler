import time
from typing import List, Optional, Tuple

from app.domain.models import Repository
from app.infrastructure.db.repository_store import save_repositories
from app.infrastructure.github.graphql_client import GitHubGraphQLClient
from app.infrastructure.github.queries import SEARCH_REPOSITORIES_QUERY


def fetch_repository_page(
    client: GitHubGraphQLClient,
    cursor: Optional[str] = None,
) -> Tuple[List[Repository], Optional[str], bool, dict]:
    response = client.execute(
        SEARCH_REPOSITORIES_QUERY,
        variables={"cursor": cursor},
    )

    data = response["data"]
    search_data = data["search"]
    page_info = search_data["pageInfo"]
    nodes = search_data["nodes"]
    rate_limit = data.get("rateLimit", {})

    repositories = []
    for node in nodes:
        if not node:
            continue

        repositories.append(
            Repository(
                github_id=node["id"],
                repository_name=node["name"],
                owner_login=node["owner"]["login"],
                repository_url=node["url"],
                stars_count=node["stargazerCount"],
            )
        )

    return repositories, page_info["endCursor"], page_info["hasNextPage"], rate_limit


def crawl_and_store_repositories(
    connection,
    client: GitHubGraphQLClient,
    target_count: int = 100_000,
    page_size: int = 100,
    sleep_seconds: float = 0.2,
) -> int:
    del page_size  # fixed by GraphQL query: first: 100

    total_saved = 0
    cursor = None
    has_next_page = True

    while has_next_page and total_saved < target_count:
        repositories, cursor, has_next_page, rate_limit = fetch_repository_page(
            client=client,
            cursor=cursor,
        )

        if not repositories:
            break

        remaining_needed = target_count - total_saved
        batch = repositories[:remaining_needed]

        save_repositories(connection, batch)
        total_saved += len(batch)

        remaining = rate_limit.get("remaining")
        cost = rate_limit.get("cost")
        reset_at = rate_limit.get("resetAt")

        print(
            f"Saved batch={len(batch)} total_saved={total_saved} "
            f"rate_limit_remaining={remaining} cost={cost} reset_at={reset_at}"
        )

        if total_saved < target_count and has_next_page:
            time.sleep(sleep_seconds)

    return total_saved