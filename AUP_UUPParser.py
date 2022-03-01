import json
import sys
from datetime import datetime

import pandas as pd
import requests
from github import Github


def uploadtoGithub(data, name):
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


def mergetimes(area_df):
    RSA = area_df["RSA"][0]

    merged_df = pd.DataFrame()
    times = []
    starts = list(area_df["UNT"])
    ends = list(area_df["WEF"])
    times.extend(starts)
    times.extend(ends)
    times = set(times)
    times = list(times)
    times.sort()

    time = 0
    Exit = len(times)

    # For each time block
    while time < Exit - 1:
        # Get current time block
        block_start = times[time]
        block_end = times[time + 1]

        # Initialize block FL
        low = sys.maxsize
        high = 0

        # Check all entries of the same RSA
        for index, row in area_df.iterrows():
            area_start = row["WEF"]
            area_end = row["UNT"]

            area_low = row["MNM FL"]
            area_high = row["MAX FL"]

            # If entry is within our time frame amend FL-block
            if area_start <= block_start and area_end >= block_end:
                if area_low < low:
                    low = area_low
                if area_high > high:
                    high = area_high

        row = {"RSA": RSA, "WEF": block_start, "UNT": block_end, "MNM FL": low, "MAX FL": high}

        # If block-FL not altered, area was not active thus not appened
        if high != 0 and low != sys.maxsize:
            # Add data for this time block
            merged_df = merged_df.append(row, ignore_index=True)

        time += 1

    return merged_df  # All the data of each time block for one RSA


def writeAreas(area, countries):
    # For all the data of each time block of one RSA
    for index, row in area.iterrows():
        # RSA,NOTAM,REMARK,MNM FL,MAX FL,WEF,UNT,FUA/EU RS,FIR,UIR
        try:  # To get data
            AreaName = row["RSA"]
            SchedStartDate = datetime.today().strftime('%m%d')
            SchedEndDate = datetime.today().strftime('%m%d')
            SchedWeekdays = datetime.today().weekday() + 1
            StartTime = "".join(row["WEF"].split(":"))
            EndTime = "".join(row["UNT"].split(":"))
            Lower = int(row["MNM FL"]) * 100
            Upper = int(row["MAX FL"]) * 100

            row = f"{AreaName}:{SchedStartDate}:{SchedEndDate}:{SchedWeekdays}:{StartTime}:{EndTime}:{Lower}:{Upper}:AUP/UUP\n"
            print(row)
            # Save data
            for country in countries.keys():
                if AreaName.startswith(countries[country]["Code"]):
                    countries[country]["Data"] += row

        except Exception as e:
            print("Couldn't read data on row ", index)

    return countries


def parseAreas(countries, data):
    # Initialize
    name = data["RSA"][0]
    temp = pd.DataFrame()

    # For every row in the csv
    for index, row in data[:15].iterrows():
        # If area is the same, add it
        if row["RSA"] == name:
            temp = temp.append(row, ignore_index=True)

        # If area is different, parse the previous area's entries and initialize a a clean df afterwards with current area
        else:
            areas = mergetimes(temp)
            countries = writeAreas(areas, countries)
            temp = pd.DataFrame().append(row, ignore_index=True)

        name = row["RSA"]


def main():
    try:
        countries = json.loads(
            requests.get("https://raw.githubusercontent.com/MatisseBE/VATSIMareas/main/Countries.txt").text)
        data = pd.read_csv("areas.csv")

    except Exception as e:
        print("Could not get countries or data from Github")
        print(e.args)

    # Parse data
    parseAreas(countries, data)

    # Upload data
    for country in countries.keys():
        print(countries[country]["Data"])
        # uploadtoGithub(countries[country]["Data"], "Datafiles/%s.txt" % (country))


if __name__ == '__main__':
    main()
