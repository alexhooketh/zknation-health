from matplotlib import pyplot
from random import choices
import requests

delegates = requests.post("https://api.tally.xyz/query", json={
    "query": """
    query Delegates($input: DelegatesInput!) {
  delegates(input: $input) {
    nodes {
      ... on Delegate {
        id
        account {
          address
          bio
          name
          picture
          twitter
        }
        votesCount
        delegatorsCount
        statement {
          statementSummary
        }
        token {
          symbol
          decimals
        }
      }
    }
    pageInfo {
      firstCursor
      lastCursor
    }
  }
}
    """,
    "variables": {
        "input": {
            "filters": {
                "organizationId": "2297436623035434412"
            },
            "page": {
                "limit": 100
            },
            "sort": {
                "isDescending": True,
                "sortBy": "votes"
            }
        }
    }
}, headers={"Api-Key": "365b418f59bd6dc4a0d7f23c2e8c12d982f156e9069695a6f0a2dcc3232448df"}).json()

total_votes = int(requests.post("https://api.tally.xyz/query", json={
    "query": "\n    query OrganizationDelegatesSummary($input: OrganizationInput!) {\n  organization(input: $input) {\n    delegatesVotesCount\n    tokenIds\n  }\n}\n    ",
    "variables": {
        "input": {
            "id":"2297436623035434412"
        }
    }
}, headers={"Api-Key": "365b418f59bd6dc4a0d7f23c2e8c12d982f156e9069695a6f0a2dcc3232448df"}).json()["data"]["organization"]["delegatesVotesCount"])//10**18

top = [int(x["votesCount"])//10**18 for x in delegates["data"]["delegates"]["nodes"]]
labels = [x["account"]["name"] for x in delegates["data"]["delegates"]["nodes"]]
top.append(total_votes-sum(top))
labels.append("Others")

pyplot.style.use("ggplot")
fig = pyplot.figure(figsize=(10, 10))
pyplot.pie(top, labels=labels, autopct="%1.1f%%", startangle=90, counterclock=False)
pyplot.show()