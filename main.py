from github import Github
import pandas as pd
import os


def get_forks(base_repo):
    for fork_repo in base_repo.get_forks():
        # noinspection PyBroadException1,PyBroadException
        try:
            if base_repo.compare(base_repo.default_branch,
                                 fork_repo.owner.login + ":" + fork_repo.default_branch).ahead_by > 0:
                data.append(
                    [fork_repo.owner.login, fork_repo.name, fork_repo.html_url,
                     fork_repo.get_branch(
                         fork_repo.default_branch).commit.commit.author.date, 'true'])
                get_forks(fork_repo)
        except Exception:
            pass


# search github
gh = Github(os.environ.get("ACCESS_TOKEN"))
searchResult = gh.search_code(query='IDalamudPlugin language:C#')

# extract repos from search result
data = []
for repo in searchResult:
    data.append([repo.repository.owner.login, repo.repository.name, repo.repository.html_url,
                 repo.repository.get_branch(repo.repository.default_branch).commit.commit.author.date, 'false'])
    get_forks(repo.repository)

# create df
df = pd.DataFrame(data, columns=['Author', 'Name', 'URL', 'LastUpdated', 'IsFork'])

# remove dupes
df = df.drop_duplicates()

# remove blacklisted matches (e.g. dalamud, false positives, test projects)
dfd = pd.read_csv('docs/_data/blacklist.csv', header=None, names=['Name'])
blacklist = dfd.Name.tolist()
df = df[~df.Name.isin(blacklist)]

# sort by last updated, fork
df.sort_values(['LastUpdated', 'IsFork'], ascending=[False, True], inplace=True)

# update forks
df.loc[df.IsFork == 'true', 'Name'] = df['Name'] + ' (fork)'
del df['IsFork']

# remove timestamps for cleaner table
df['LastUpdated'] = pd.to_datetime(df['LastUpdated']).dt.date

# write result to csv
df.to_csv('docs/_data/repos.csv', index=False)
