# GitHub Crawler

A GitHub repository crawler built for a software engineering assignment.
The project uses the **GitHub GraphQL API** to fetch repository star counts, stores the data in **PostgreSQL**, and runs automatically through **GitHub Actions** using a Postgres service container.

---

## Objective

The goal of this project is to:

* Crawl **GitHub repositories and their star counts**
* Store the data in a **PostgreSQL database**
* Run the crawler inside a **GitHub Actions pipeline**
* Export the crawled data as **artifacts (CSV and SQL dump)**

The implementation demonstrates API integration, pagination, database design, CI pipelines, and scalable architecture.

---

## Tech Stack

* **Python 3.11**
* **GitHub GraphQL API**
* **PostgreSQL**
* **GitHub Actions**
* **psycopg2**
* **requests**

---

## Project Structure

```
.github/workflows/
  crawler.yml

app/
  domain/
    models.py

  application/
    crawl_repositories.py

  infrastructure/
    github/
      graphql_client.py
      queries.py

    db/
      connection.py
      repository_store.py
      schema.sql

  main.py

requirements.txt
README.md
```

---

## Architecture Overview

The project follows a simple clean architecture approach.

### Domain

Contains the core data model.

Example:

* `Repository` model representing GitHub repositories.

### Application Layer

Contains the main crawl use-case logic:

* Fetch repositories using the GitHub GraphQL API
* Handle pagination
* Convert API responses to domain objects
* Store them in the database

### Infrastructure Layer

Handles integrations:

* GitHub API client
* PostgreSQL connection
* Database persistence layer

This separation improves maintainability and keeps API details isolated from business logic.

---

## Database Schema

Repositories are stored in the table:

```
github_crawler.repositories
```

Columns:

| Column          | Description                         |
| --------------- | ----------------------------------- |
| github_id       | Unique repository ID                |
| repository_name | Repository name                     |
| owner_login     | Repository owner                    |
| repository_url  | Repository URL                      |
| stars_count     | Number of stars                     |
| crawled_at      | Timestamp when the repo was crawled |
| updated_at      | Last update timestamp               |

### Upsert Strategy

The crawler uses:

```
ON CONFLICT (github_id) DO UPDATE
```

This allows the crawler to run repeatedly while efficiently updating star counts without creating duplicates.

---

## GitHub GraphQL Crawling

The crawler queries GitHub’s GraphQL API and retrieves repositories using cursor-based pagination.

Each request fetches up to:

```
100 repositories per request
```

The crawler continues fetching pages until the desired number of repositories is reached.

The query retrieves:

* repository ID
* repository name
* owner login
* repository URL
* stargazer count

---

## Rate Limit Handling

GitHub GraphQL enforces rate limits.

The crawler includes:

* retry logic
* exponential backoff
* rate limit monitoring

This ensures the crawler respects GitHub API limits.

---

## GitHub Actions Pipeline

The project includes a CI pipeline that:

1. Starts a **PostgreSQL service container**
2. Installs Python dependencies
3. Creates database schema
4. Runs the crawler
5. Exports the database
6. Uploads results as artifacts

Artifacts generated:

* `repositories.csv`
* `github_crawler_dump.sql`

---

## Running the Project

The project is designed to run through **GitHub Actions**.

Steps:

1. Push the repository to GitHub
2. Open the **Actions** tab
3. Run the **GitHub Repo Crawler** workflow

After completion, artifacts can be downloaded from the workflow run.

---

## Scaling to 500 Million Repositories

If this crawler needed to process **hundreds of millions of repositories**, the architecture would change significantly.

Key improvements:

### Distributed Crawling

Instead of a single process, use distributed workers with a queue system such as:

* Kafka
* RabbitMQ
* AWS SQS

### Horizontal Scaling

Multiple crawler workers would run in parallel, each responsible for different repository ranges.

### Data Storage

A single PostgreSQL instance may not scale. Alternatives include:

* Postgres sharding
* Citus
* BigQuery
* ClickHouse

### Batch Ingestion

Large datasets should be written using bulk operations like:

```
COPY
```

or large batch inserts instead of row-by-row writes.

---

## Schema Evolution

Future metadata may include:

* Issues
* Pull Requests
* Comments
* Reviews
* CI checks
* Commits

Instead of extending the repository table, separate tables should be created:

```
repositories
pull_requests
issues
comments
reviews
checks
commits
```

This allows efficient updates.

Example:

If a PR receives new comments tomorrow, only new comment rows are inserted instead of rewriting the entire PR record.

---

## Example Output

The crawler produces a CSV file similar to:

```
github_id, repository_name, owner_login, repository_url, stars_count
```

Each row represents a GitHub repository and its star count.

---

## Author

Saad Ahmed Khan
