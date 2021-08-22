from github import Github
import pandas as pd
import os

# search github
gh = Github(os.environ.get("ACCESS_TOKEN"))
searchResult = gh.search_code(query='IDalamudPlugin language:C#')

# extract repos from search result
data = []
for repo in searchResult:
    commit_author_date = repo.repository.get_branch(repo.repository.default_branch).commit.commit.author.date
    data.append([repo.repository.owner.login, repo.repository.name, repo.repository.html_url,
                 commit_author_date, 'false'])
    for repoFork in repo.repository.get_forks():
        # noinspection PyBroadException
        try:
            if repo.repository.compare(repo.repository.default_branch,
                                       repoFork.owner.login + ":" + repoFork.default_branch).ahead_by > 0:
                commit_author_date = repoFork.get_branch(
                    repoFork.default_branch).commit.commit.author.date
                data.append([repoFork.owner.login, repoFork.name, repoFork.html_url, commit_author_date, 'true'])
        except Exception:
            pass

# create df
df = pd.DataFrame(data, columns=['Author', 'Name', 'URL', 'LastUpdated', 'IsFork'])

# remove dupes
df = df.drop_duplicates()

# remove blacklisted matches (e.g. dalamud, false positives, test projects)
dfd = pd.read_csv('docs/_data/blacklist.csv', header=None, names=['Name'])
blacklist = dfd.Name.tolist()
df = df[~df.Name.isin(blacklist)]

# sort by last updated
df.sort_values(by=['LastUpdated'], inplace=True, ascending=False)

# update forks
df.loc[df.IsFork == 'true', 'Name'] = df['Name'] + ' (fork)'
del df['IsFork']

# remove timestamps for cleaner table
df['LastUpdated'] = pd.to_datetime(df['LastUpdated']).dt.date

# write result to csv
df.to_csv('docs/_data/repos.csv', index=False)
