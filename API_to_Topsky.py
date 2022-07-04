import requests
import json
import pandas as pd
from datetime import datetime
from datetime import timedelta
import sys

def CreateTimeBlocks(temp):
    RSA = temp["RSA"].iloc[0]

    parsed_df = pd.DataFrame(columns=["RSA","WEF","UNT","MNM FL","MAX FL"])
    times = []
    starts = list(temp["UNT"])
    ends = list(temp["WEF"])
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
        for index, row in temp.iterrows():
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
            #parsed_df = parsed_df.append(row,ignore_index=True)      
            parsed_df.loc[len(parsed_df)] = [RSA,block_start,block_end,low,high]
        time += 1 #Go to the next time block

    return parsed_df #All the data of each time block for one RSA

def writeAreas(area):
    data_one_RSA = ""
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
        data_one_RSA += row
      
      except Exception as e:
          print("Couldn't read data on row ", index)
          print(e.args)

    return data_one_RSA

def Parsedates(area):
    date = datetime.today().strftime('%Y-%m-%d')
    area["start_time"] = datetime.strptime('%s %s' % (date,area["start_time"]), '%Y-%m-%d %H:%M:%S')
    area["end_time"] = datetime.strptime('%s %s' % (date,area["end_time"]), '%Y-%m-%d %H:%M:%S')
    midnight = datetime.strptime('%s %s' % (date,"00:00"), '%Y-%m-%d %H:%M') 
    if area["start_time"] >= area["end_time"] and area["end_time"] >= midnight: #Later than midnight is next day, but only if start time later than end (Otherwise later than midnight is same day)(Same time means active all day)
        area["end_time"] += timedelta(days=1)
    return area

topsky_data = ""

temp = pd.DataFrame(columns=["RSA","WEF","UNT","MNM FL","MAX FL"])


for neighbourg in ["EB","EH","LF","ED"]:
    data_raw = requests.get("https://eaup.ambitio.cyou/%s" % (neighbourg)).text
    data = json.loads(data_raw)

    name = data["areas"][0]["name"]


    for area in data["areas"]:     
        area = Parsedates(area)

        #If area is the same, add it
        if area["name"] == name:
            temp.loc[len(temp)] = [area["name"],area["start_time"],area["end_time"],area["minimum_fl"],area["maximum_fl"]]

        #If area is different, parse the previous entries first, then initialize a a clean df with current entry
        else:
            areas = CreateTimeBlocks(temp)
            topsky_data += writeAreas(areas)
            temp = pd.DataFrame(columns=["RSA","WEF","UNT","MNM FL","MAX FL"])
            temp.loc[0] = [area["name"],area["start_time"],area["end_time"],area["minimum_fl"],area["maximum_fl"]]

        name = area["name"]


with open("./topsky_data.txt","w") as file:
    file.write(topsky_data)

print(topsky_data)
print("Data valid until", data["notice_info"]["valid_til"])



