from app.application.crawl_repositories import crawl_and_store_repositories
from app.infrastructure.db.connection import get_db_connection
from app.infrastructure.github.graphql_client import GitHubGraphQLClient


def main() -> None:
    connection = get_db_connection()
    try:
        client = GitHubGraphQLClient()
        total_saved = crawl_and_store_repositories(
            connection=connection,
            client=client,
            target_count=100_000,
        )
        print(f"Finished crawl. Total repositories saved: {total_saved}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()