from numpy import block
import pandas as pd
from datetime import datetime
from datetime import timedelta
from github import Github
import requests
import json
import sys

def uploadtoGithub(data, name):
    #Github token
    with open("token.txt","r") as file: 
        token = file.read()

    g = Github(token)

    repo = g.get_user().get_repo("vLARA")
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
        repo.update_file(contents.path, "%s" % (datetime.today().strftime('%Y-%m-%d-%H:%M')), content, contents.sha , branch="main")
        print(git_file + ' UPDATED ' + str(datetime.now()))
    else:
        repo.create_file(git_file, "committing files", content, branch="main")
        print(git_file + ' CREATED ' + str(datetime.now()))

def CreateTimeBlocks(area_df):
    RSA = area_df["RSA"][0]

    parsed_df = pd.DataFrame()
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

    #For each time block
    while time < Exit-1:
        #Get current time block
        block_start = times[time]
        block_end = times[time+1]
        
        #Initialize block FL
        low = sys.maxsize
        high = 0

        #Check all entries of the same RSA
        for index, row in area_df.iterrows():
            area_start = row["WEF"]
            area_end = row["UNT"]

            if str(int(row["MNM FL"])).lstrip('0') == "": # "0" ==> ""
                area_low = 0
            else:
                area_low = int(str(int(row["MNM FL"])).lstrip('0')) #"095" ==> 95


            if str(int(row["MAX FL"])).lstrip('0') == "": 
                area_high = 0
            else:
                area_high = int(str(int(row["MAX FL"])).lstrip('0'))


            #If entry is within our time frame amend FL-block
            if area_start <= block_start and area_end >= block_end:
            #if block_start <= area_start and area_end <= block_end:
                if area_low < low:
                    low = area_low
                if area_high > high:
                    high = area_high

        row = {"RSA" : RSA, "WEF" :  block_start, "UNT" :block_end, "MNM FL":low, "MAX FL": high }
        #print(row)

        #If the block-FL not altered and remained max,0 then the area never became active. There's a break between activation times therefore we do not append
        if high != 0 and low != sys.maxsize:
            #Add data for this time block
            parsed_df = parsed_df.append(row,ignore_index=True)      
        
        time += 1 #Go to the next time block

    return parsed_df #All the data of each time block for one RSA

def writeAreas(area,countries):
    #For all the data of each time block of one RSA
    #RSA,NOTAM,REMARK,MNM FL,MAX FL,WEF,UNT,FUA/EU RS,FIR,UIR
    for index, row in area.iterrows():
      try: #To get data
        
        AreaName = row["RSA"]        
        SchedStartDate = row["WEF"].strftime('%m%d')
        SchedEndDate = row["UNT"].strftime('%m%d')

        StartTime = row["WEF"].strftime('%H%M')
        EndTime = row["UNT"].strftime('%H%M')

        SchedWeekdays = datetime.today().weekday() + 1

        Lower = int(row["MNM FL"])*100
        Upper = int(row["MAX FL"])*100

        row = f"{AreaName}:{SchedStartDate}:{SchedEndDate}:{SchedWeekdays}:{StartTime}:{EndTime}:{Lower}:{Upper}:AUP/UUP\n"
        #print(row)
        
        #Save data
        for country in countries.keys():
            if AreaName.startswith(countries[country]["Code"]):
                countries[country]["Data"] += row
      
      except Exception as e:
          print("Couldn't read data on row ", index)

    return countries

def Parsedates(row):
    date = datetime.today().strftime('%Y-%m-%d')
    row["WEF"] = datetime.strptime('%s %s' % (date,row["WEF"]), '%Y-%m-%d %H:%M')
    row["UNT"] = datetime.strptime('%s %s' % (date,row["UNT"]), '%Y-%m-%d %H:%M')
    midnight = datetime.strptime('%s %s' % (date,"00:00"), '%Y-%m-%d %H:%M') 
    if row["WEF"] >= row["UNT"] and row["UNT"] >= midnight: #Later than midnight is next day, but only if start time later than end (Otherwise later than midnight is same day)(Same time means active all day)
        row["UNT"] += timedelta(days=1)

    return row

def parseAreas(countries,data):
    #Initialize
    name = data["RSA"][0]
    temp = pd.DataFrame()

    #For every row in the csv
    for index, row in data.iterrows():
        try:
            row = Parsedates(row)

            #If area is the same, add it
            if row["RSA"] == name:
                temp = temp.append(row,ignore_index=True)
                #print("Added to previous")
            
            #If area is different, parse the previous entries first, then initialize a a clean df with current entry
            else:
                #print("Different from previous")
                areas = CreateTimeBlocks(temp)
                countries = writeAreas(areas,countries)
                temp = pd.DataFrame().append(row,ignore_index=True)
        except:
            print("Error with row", index)
        finally:
            name = row["RSA"]
        

try:
    countries = json.loads(requests.get("https://raw.githubusercontent.com/MatisseBE/vLARA/main/Countries.txt").text)
    data = pd.read_csv("areas.csv") 

except Exception as e:
    print("Could not get countries or data from Github")
    print(e.args)

#Parse data
parseAreas(countries,data)

#Upload data
for country in countries.keys():
    uploadtoGithub(countries[country]["Data"],"Datafiles/%s.txt" % (country))
