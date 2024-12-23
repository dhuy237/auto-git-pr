import os
from time import *
from os import path
from git import Repo
from git_credentials.key import GIT_TOKEN
import requests
import json

DIR_PATH = "/Users/huy.tran/Documents/personal_repos/auto-git-pr"
REPO_REMOTE_PATH = "https://github.com/dhuy237/auto-git-pr.git"
DEV_BRANCH = "dev"
REPO_URL = "https://api.github.com/repos/dhuy237/auto-git-pr/pulls"

def commit_files():
    repo = Repo(DIR_PATH)
    if repo != None:
        new_branch = DEV_BRANCH
        current = repo.create_head(new_branch)
        current.checkout()
        master = repo.heads.main
        repo.git.pull('origin', master)
        #creating file
        dtime = strftime('%d-%m-%Y %H:%M:%S', localtime())
        with open(DIR_PATH + path.sep + 'lastCommit' + '.txt', 'w') as f:
            f.write(str(dtime))
        if not path.exists(DIR_PATH):
            os.makedirs(DIR_PATH)
        print('file created---------------------')

        if repo.index.diff(None) or repo.untracked_files:

            repo.git.add(A=True)
            repo.git.commit(m='auto commit at {}'.format(dtime))
            repo.git.push('--set-upstream', 'origin', current)
            print('git push')
        else:
            print('no changes')

# commit_files()

def create_pull_request(
    title,
    body,
    base="main",
    head=DEV_BRANCH,
    token=GIT_TOKEN,
):
    headers = {"Authorization": "Bearer %s" % token,
            'Content-Type': 'application/vnd.github+json'}
    data = {
            "title": title,
            "base": base,
            "head": head
    }
    if body:
        data["body"] = body
    
    response = requests.post(
        REPO_URL,
        headers=headers,
        data=json.dumps(data),
        verify=False
    )
    if response.status_code not in range(200, 299):
        raise Exception("Response %d: %s" % (response.status_code,
                                             response.content))
    return response.json()

response = create_pull_request(
    title="Test Auto-PR",
    body="This is an automatically created PR."
)
print(response)