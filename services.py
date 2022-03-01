from datetime import datetime

import requests
from github import Github


def get_countries_from_github(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def upload_to_github(data, name):
    # Github token
    with open("token.txt", "r") as file:
        token = file.read()

    g = Github(token)

    repo = g.get_user().get_repo("VATSIMareas")
    all_files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="', '').replace('")', ''))

    content = data

    git_file = name
    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "%s" % (datetime.today().strftime('%Y-%m-%d-%H:%M')), content, contents.sha,
                         branch="main")
        print(git_file + ' UPDATED ' + str(datetime.now()))
    else:
        repo.create_file(git_file, "committing files", content, branch="main")
        print(git_file + ' CREATED ' + str(datetime.now()))
