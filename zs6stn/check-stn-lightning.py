### https://pypi.org/project/weatherbug-spark/
import asyncio
import weatherbug_spark
import json
from datetime import datetime

class LightningStats:
    def __init__(self, closestPulseDistance, closestPulseDirection, shortMessage):
        self.closestPulseDistance = closestPulseDistance
        self.closestPulseDirection = closestPulseDirection
        self.batch = shortMessage

    def shortMessage(self):
        return self.shortMessage

    def closestPulseDistanceKm(self, roundValue = True):
        if (roundValue == True):
            return round((self.closestPulseDistance * 1.60934), 2)
        else:
            return self.closestPulseDistance * 1.60934

    def closestPulseDirectionCardinal(self):
        dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        ix = round(self.closestPulseDirection / (360. / len(dirs)))
        return ix

async def main():
    direction = {
        "N" : "North",
        "NNE" : "North North East",
        "NE" : "North East",
        "ENE" : "East North East",
        "E" : "East",
        "ESE" : "East South East",
        "SE" : "South East",
        "SSE" : "South South East",
        "S" : "South",
        "SSW" : "South South West",
        "WSW" : "West South West",
        "W" : "West",
        "WNW" : "West North West",
        "NW" : "North West",
        "NNW" : "North North West"
    }
#    print("WeatherBug Lightning Collector")
    data = await weatherbug_spark.get_data(lat=-26.0577, lon=28.0252)
    stats = LightningStats(data.closestPulseDistance, data.closestPulseDirection, data.shortMessage)

    # DateTime Now
#    print(datetime.now())

    # Get the closest strike distance
#    print(round(data.closestPulseDistance * 1.60934, 2)) # float
    # print(stats.closestPulseDistanceKm())

    # Get The closest lightning strike direction in degrees.
    # print(data.closestPulseDirection)
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    ix = round(data.closestPulseDirection / (360. / len(dirs)))
 #   print(dirs[ix % len(dirs)])
    # print(stats.closestPulseDirectionCardinal)

    # Get the local lightning strike locations
    # print(data.pulseListAlert) # List of LightningStrike objects

    # Get the global lightning strike locations
    # print(data.pulseListGlobal) # List of LightningStrike objects

    # Get the short message
 #   print(data.shortMessage) # Monitor Storms
    # print(stats.shortMessage())

    # Get the long message
 #   print(data.safetyMessage) # You are not in immediate danger now, but stay alert and frequently check WeatherBug ...

    # Get the hex code for the color of the alert
    #print(data.alertColor) # #F0D701
    #print(json.dumps(stats.))
    if (int(round(data.closestPulseDistance * 1.60934, 0)) <= 15):
        print("Lightning Warning!",data.shortMessage, ", ", int(round(data.closestPulseDistance * 1.60934, 0)), "Kilometers away, ", direction[dirs[ix % len(dirs)]], " from Sandton, from Zulu Sierra Six, Sierra Tango November")
    else:
        print("No Lightning",data.shortMessage, ", ", int(round(data.closestPulseDistance * 1.60934, 0)), "Kilometers away, ", direction[dirs[ix % len(dirs)]], " from Sandton, from Zulu Sierra Six, Sierra Tango November")

if __name__ == "__main__":
    asyncio.run(main())
