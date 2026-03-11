SEARCH_REPOSITORIES_QUERY = """
query SearchRepositories($cursor: String) {
  search(
    query: "stars:>0"
    type: REPOSITORY
    first: 100
    after: $cursor
  ) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        id
        name
        url
        stargazerCount
        owner {
          login
        }
      }
    }
  }
  rateLimit {
    cost
    remaining
    resetAt
  }
}
"""