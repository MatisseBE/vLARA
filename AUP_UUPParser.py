import pandas as pd
from datetime import datetime
from github import Github
import requests
import json

def uploadtoGithub(data, name):
    #Github token
    with open("token.txt","r") as file: 
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
            all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

    content = data

    git_file = name
    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "committing files", content, contents.sha , branch="main")
        print(git_file + ' UPDATED ' + str(datetime.now()))
    else:
        repo.create_file(git_file, "committing files", content, branch="main")
        print(git_file + ' CREATED ' + str(datetime.now()))

def parseAreas(countries,data):
    for index, row in data.iterrows():
    #RSA,NOTAM,REMARK,MNM FL,MAX FL,WEF,UNT,FUA/EU RS,FIR,UIR

      try:
        AreaName = row["RSA"]
        SchedStartDate = datetime.today().strftime('%m%d')
        SchedEndDate = datetime.today().strftime('%m%d')
        SchedWeekdays = datetime.today().weekday() + 1
        StartTime = "".join(row["WEF"].split(":"))
        EndTime = "".join(row["UNT"].split(":"))
        Lower = int(row["MNM FL"])*100
        Upper = int(row["MAX FL"])*100

        row = f"{AreaName}:{SchedStartDate}:{SchedEndDate}:{SchedWeekdays}:{StartTime}:{EndTime}:{Lower}:{Upper}\n"


        for country in countries.keys():
            if AreaName.startswith(countries[country]["Code"]):
                countries[country]["Data"] += row
      except:
          print("Couldn't read data on row ", index)
    

try:
    countries = json.loads(requests.get("https://raw.githubusercontent.com/MatisseBE/VATSIMareas/main/Countries.txt").text)
    data = pd.read_csv("https://raw.githubusercontent.com/MatisseBE/VATSIMareas/main/areas.csv")

except:
    print("Could not get countries or data from Github")

#Parse data
parseAreas(countries,data)

#Upload data
for country in countries.keys():
    uploadtoGithub(countries[country]["Data"],"Datafiles/%s.txt" % (country))

