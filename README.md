# VATSIM Areas


## What?
![image](https://user-images.githubusercontent.com/51272243/155607854-d5804a5c-61ac-458e-a4ce-35e3b84a51b9.png)

## Why
VATSIM and its controllers operate under the slogan "As Real As It Gets". Not so long ago controllers did not open any RSAs (Restricted Airspaces) on the network. Recently, through plugins, controllers were able to hardcode RSA activation times or dynimically active areas through NOTAMs. For the first time ever, we could simulate flight restrictions and make our lives more miserable. In real life however, more areas were open than we were able predict or extract. These gaps should be covered now.  

## Limitations
Parsed in time blocks, could need further merging if consecutive FL-blocks are equal.

TODO: Find host

TODO: Update robot to extract parser code from github so it can be remotely updated.

## Those other files?
**AUP_UUPParser.py**

Converts the online table into the plugin format and uploads them to Github automatically.


**Countries.txt**

You can make a pull request to add your country to the list. If the data source does not cover your area however, an empty datafile will be created. 

## Note
All data provided by EC NM.

For flightsimulation only!

Made with love ❤, and a lot of cookies 🍪

