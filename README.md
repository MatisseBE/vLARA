# VATSIM Areas


## What?
![image](https://user-images.githubusercontent.com/51272243/156027169-153881ad-8caf-429f-8737-2e327f75567a.png)

## Why
VATSIM and its controllers operate under the slogan "As Real As It Gets". Not so long ago controllers did not open any RSAs (Restricted Airspaces) on the network. Recently, through plugins, controllers were able to hardcode RSA activation times or dynimically active areas through NOTAMs. For the first time ever, we could simulate flight restrictions and make our lives more miserable. In real life however, more areas were open than we were able predict or extract. These gaps should be covered now.  

## Limitations
Successive time-blocks of RSA with identical FL-blocks may still be separated entries. This poses no problems to the plugin.

Under normal circumstances the data gets updated once every morning. This is no guarentee however until there's a host device for the project.

TODO: Remove buffer zones (ending with Z)

## How
Until proper plugin integration, I advise downloading your relevant areas before opening Euroscope and putting them into the "TopskyAreasManualAct.txt" file. In short, we use this new file as an extention to the normal areas file. If done correctly, a popup will show "TopskyAreasManualAct file in use" upon launching Euroscope.

## Those other files?
**AUP_UUPParser.py**

Converts the online table into the plugin format and uploads them to Github automatically.


**Countries.txt**

You can make a pull request to add your country to the list. If the data source does not cover your area however, an empty datafile will be created. 

## Note
All data provided by EC NM.

For flightsimulation only!

Made with love ❤, and a lot of cookies 🍪

