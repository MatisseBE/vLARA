# Virtual Local and sub-Regional Airspace management support system (vLARA)

# Update
API can now be found here:
https://eaup.vatsim.pt/api/docs


Gitlab project:
https://gitlab.com/portugal-vacc/eaup

**Looking for a front end web dev to visualise areas (Gantt charts and geo maps). Please get in touch if you are interested.**


## What?
![image](https://user-images.githubusercontent.com/51272243/159242206-294ff5c4-ec67-424d-b993-c40feb0ce1f8.png)

## Why
VATSIM and its controllers operate under the slogan "As Real As It Gets". Not so long ago controllers did not open any RSAs (Restricted Airspaces) on the network. Recently, through plugins, controllers were able to hardcode RSA activation times or dynimically active areas through NOTAMs. For the first time ever, we could simulate flight restrictions and make our lives more miserable. In real life however, more areas were open than we were able predict or extract. These gaps should be covered now.  

## Update
From now on we will be using these API endpoints:
* https://eaup.ambitio.cyou/eb
* https://eaup.ambitio.cyou/topsky/eb
* https://eaup.ambitio.cyou/raw

As a result, this repositoy is deprecated and only exist for future reference and archiving purposes.
For active developpement and documentation on the API endpoints, navigate [here](https://gitlab.com/portugal-vacc/eaup/).

## Limitations
Successive time-blocks of RSA with identical FL-blocks may still be separated entries. This poses no problems to the plugin.

Under normal circumstances the data gets updated once every morning. This is no guarentee however until there's a host device for the project.

## How
Until proper plugin integration, I advise downloading your relevant areas before opening Euroscope and putting them into the "TopskyAreasManualAct.txt" file. In short, we use this new file as an extention to the normal areas file. If done correctly, a popup will show "TopskyAreasManualAct file in use" upon launching Euroscope.

## Those other files?
**AUP_UUPParser.py**

Converts the online table into the plugin format and uploads them to Github automatically.


**Countries.txt**

You can make a pull request to add your country to the list. If the data source does not cover your area however, an empty datafile will be created. 
To assess your luck, check [this link](https://www.lara-eu.org/)!

## Notes

Some entries may seem to be be included twice. Once with the expected area and once with that same area, but ending in a "Z" (RSA ID + Z). These are (Flight plan) buffer zones (aka FBZ) around the main area and are used for flightplan purposes only. You may therefor ignore them.

However some countries will only publish these FBZ to the NM. In this case you can use them to process your areas. Note that the vertical bounds in this case may differ from the actual area you are trying to simulate. This is precisely because it is a buffer zone. You can find more [here](https://www.eurocontrol.int/sites/default/files/2020-07/eurocontrol-nm-fpl-req-guidilines-v1.3.pdf) under "4.5 Flight Buffer Zone (FBZ)".

All data provided by [European AUP/UUP EUROCONTROL](https://www.public.nm.eurocontrol.int/PUBPORTAL/gateway/spec/).

Made with love ❤, and a lot of cookies 🍪

For flightsimulation only!

