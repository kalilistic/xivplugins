from github import Github
import pandas as pd
import os

# search github
gh = Github(os.environ.get("ACCESS_TOKEN"))
searchResult = gh.search_code(query='IDalamudPlugin language:C#')

# extract repos from search result
data = []
for record in searchResult:
    data.append([record.repository.owner.login, record.repository.name, record.repository.html_url,
                 record.repository.updated_at])

# create df
df = pd.DataFrame(data, columns=['Author', 'Name', 'URL', 'LastUpdated'])

# fix index
df.index.name = 'No.'
df.index += 1

# remove dupes
df = df.drop_duplicates()

# remove blacklisted matches (e.g. dalamud, false positives, test projects)
dfd = pd.read_csv('docs/_data/blacklist.csv', header=None, names=['URL'])
blacklist = dfd.URL.tolist()
df = df[~df.URL.isin(blacklist)]

# sort by last updated
df.sort_values(by=['LastUpdated'], inplace=True, ascending=False)

# remove timestamps for cleaner table
df['LastUpdated'] = pd.to_datetime(df['LastUpdated']).dt.date

# write result to csv
df.to_csv('docs/_data/repos.csv')
