import git
import datetime
import os
from time import *
from os import path
from git import Repo

DIR_PATH = "/Users/huy.tran/Documents/personal_repos/auto-git-pr"
REPO_REMOTE_PATH = "https://github.com/dhuy237/auto-git-pr.git"
DEV_BRANCH = "dev"


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
            repo.git.commit(m='auto commit at {dtime}')
            repo.git.push('--set-upstream', 'origin', current)
            print('git push')
        else:
            print('no changes')

commit_files()