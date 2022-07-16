#!/usr/bin/env python3
#############################
## https://github.com/PeZet2
#############################
import os
import datetime
import argparse
from pathlib import Path
from github import Github
from urllib.request import urlopen


def parse_args():
    parser = argparse.ArgumentParser(description='Parse input parameters')
    parser.add_argument('--user',
                        type=str,
                        help='Github username'
                        )
    parser.add_argument('--access_token',
                        type=str,
                        help='Access token for private repositories'
                        )
    return parser.parse_args()


def save_log(stri, ts=True):
    tm = datetime.datetime.now()
    strtm = tm.strftime("%Y-%m-%d %H:%M:%S")
    if ts:
        message = f"[{strtm}]: {stri}"
    else:
        message = f"{stri}"
    with open(log_file, 'a') as f:
        print(message, end='\n', file=f)


def create_dir(a_dir: str):
    if not os.path.isdir(a_dir):
        os.mkdir(a_dir)


def get_repo_list(github: Github) -> list:
    save_log(f"Fetching repos list from GitHub...")
    return [r for r in github.get_user().get_repos()]


def delete_file(file_name: str):
    if os.path.isfile(file_name):
            os.remove(file_name)


def save_repo_to_a_file(repo_list: list, repo_list_file: str):
    delete_file(repo_list_file)
    with open(repo_list_file, 'at') as f:
        save_log(f"Saving download urls for all repos to {repo_list_file}...")
        for repo in repo_list:
            f.write(repo.get_archive_link('zipball') + "\n")
    save_log("Urls saved")


def download_repo(repo_name: str, url: str):
    save_log(f"Downloading repository: {repo_name}...")

    response = urlopen(url)
    zip_filename = download_dir + '/' + repo_name + '.zip'

    with open(zip_filename, 'wb') as f:
        f.write(response.read())
    save_log(f"Saved repo to {zip_filename}")


def main():
    # Utworzenie obiektu Github wraz z otrzymanym tokenem
    g = Github(args.access_token)

    # Utworzenie lokalizacji dla logow
    create_dir(log_dir)

    # Utworzenie lokalizacji archiwum
    create_dir(archive_dir)
    create_dir(download_dir)

    save_log("###########################################################", ts=False)
    save_log("####################################")
    save_log(f"Creating GitHub backup for {args.user}")

    # Pobranie listy repozytoriów z GitHub
    repo_list = get_repo_list(g)
    save_log(f"Repositories: {len(repo_list)}")
    if len(repo_list) == 0:
        save_log("ERR: No repositories to backup!!!")
        exit(1)

    # Zapisanie linków pobierających repozytoria do pliku
    save_repo_to_a_file(repo_list, download_repo_list_file)

    # Pobieranie repozytoriów do archiwum
    for r in repo_list:
        download_repo(r.name, r.get_archive_link('zipball'))

    save_log("End of script")


if __name__ == "__main__":
    home = f"{Path.home()}"
    archive_dir = f"{home}/archive"
    download_dir = f"{archive_dir}/github"
    download_repo_list_file = f"{download_dir}/repo_list.txt"
    log_dir = f"{home}/log"
    log_file = f"{log_dir}/github_backuper.log"

    args = parse_args()
    main()
