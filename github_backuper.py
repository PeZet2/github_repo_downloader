#!/usr/bin/env python3

#############################
## https://github.com/PeZet2
#############################

import os
import datetime
from urllib.request import urlopen
from pathlib import Path
from github import Github

USER="PeZet2"
access_token=""

home = f"{Path.home()}"
archive_dir=f"{home}/archive"
download_dir=f"{archive_dir}/github"
download_repo_list_file=f"{download_dir}/repo_list.txt"
log_dir = f"{home}/log"
log_file=f"{log_dir}/github_backuper.log"

g = Github(access_token)

master_branch="master"
main_branch="main"

def saveLog(stri, ts=True):
    tm = datetime.datetime.now()
    strtm = tm.strftime("%Y-%m-%d %H:%M:%S")
    if ts == True:
        message = f"[{strtm}]: {stri}"
    else:
        message = f"{stri}"
    with open(log_file, 'a') as f:
        print(message, end='\n', file=f)


def create_dir(a_dir: str):
    if (not os.path.isdir(a_dir)):
        os.mkdir(a_dir)


def get_repo_list() -> list:
    saveLog(f"Fetching repos list from GitHub...")
    return [r for r in g.get_user().get_repos()]


def delete_file(file_name: str):
    if (os.path.isfile(file_name)):
            os.remove(file_name)


def save_repo_to_a_file(repo_list: list, repo_list_file: str):
    delete_file(repo_list_file)
    with open(repo_list_file, 'at') as f:
        saveLog(f"Saving download urls for all repos to {repo_list_file}...")
        for repo in repo_list:
            f.write(repo.get_archive_link('zipball') + "\n")
    saveLog("Urls saved")


def download_repo(repo_name:str, url:str):
    saveLog(f"Downloading repository: {repo_name}...")

    response = urlopen(url)
    zip_filename = download_dir + '/' + repo_name + '.zip'

    with open(zip_filename, 'wb') as f:
        f.write(response.read())
    saveLog(f"Saved repo to {zip_filename}")



#Utworzenie lokalizacji dla logow
create_dir(log_dir)

# Utworzenie lokalizacji archiwum
create_dir(archive_dir)
create_dir(download_dir)

saveLog("###########################################################", ts=False)
saveLog("####################################")
saveLog(f"Creating GitHub backup for {USER}")

# Pobranie listy repozytoriów z GitHub
repo_list=get_repo_list()
saveLog(f"Repositories: {len(repo_list)}")
if (len(repo_list) == 0):
    saveLog("ERR: No repositories to backup!!!")
    exit(1)

# Zapisanie linków pobierających repozytoria do pliku
save_repo_to_a_file(repo_list, download_repo_list_file)

# Pobieranie repozytoriów do archiwum
for r in repo_list:
    download_repo(r.name, r.get_archive_link('zipball'))


saveLog("End of script")
