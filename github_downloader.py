#!/usr/bin/env python3
#############################
## https://github.com/PeZet2
#############################

import os
import datetime
from urllib.request import urlopen
from github import Github

USER='YOUR_USERNAME'
access_token='GENERATED_GITHUB_ACCESS_TOKEN'
download_dir='DOWNLOAD_DIR'
download_repo_list_file=download_dir + '/repo_list.txt'
log_file='LOGFILE.LOG'

g = Github(access_token)


def saveLog(stri):
    tm = datetime.datetime.now()
    strtm = tm.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, 'a') as f:
        print("["+strtm+"]: "+stri, end='\n', file=f)


def create_archive_dir(a_dir: str):
    if (not os.path.isdir(a_dir)):
        os.mkdir(a_dir)
        saveLog(f"Created archive directory at {download_dir}")


def get_repo_list() -> list:
    saveLog(f"Fetching repos list from GitHub...")
    return [r for r in g.get_user().get_repos()]


def delete_file(file_name: str):
    if (os.path.isfile(file_name)):
            os.remove(file_name)


def save_repo_list_to_a_file(repo_list: list, repo_list_file: str):
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



saveLog("$###################################")
saveLog(f"Creating GitHub backup for {USER}")

# Utworzenie lokalizacji archiwum
create_archive_dir(download_dir)

# Pobranie listy repozytoriów z GitHub
repo_list=get_repo_list()
saveLog(f"Repositories: {len(repo_list)}")
if (len(repo_list) == 0):
    saveLog("ERR: No repositories to backup!!!")
    exit(1)

# Zapisanie linków pobierających repozytoria do pliku
save_repo_list_to_a_file(repo_list, download_repo_list_file)

# Pobieranie repozytoriów do archiwum
for r in repo_list:
    download_repo(r.name, r.get_archive_link('zipball'))


saveLog("End of script")


