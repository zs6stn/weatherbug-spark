### https://pypi.org/project/weatherbug-spark/
import asyncio
import weatherbug_spark
import json
from datetime import datetime

maxPulseDistance = 15 # km

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
    "SW" : "South West",
    "WSW" : "West South West",
    "W" : "West",
    "WNW" : "West North West",
    "NW" : "North West",
    "NNW" : "North North West"
}

class LightningStats:
    def __init__(self, lat, lon, siteName):
#        self.closestPulseDistance = closestPulseDistance
#        self.closestPulseDirection = closestPulseDirection
#        self.batch = shortMessage
        self.lat = lat
        self.lon = lon
        self.siteName = siteName
        self.closestPulseDistance = 100

    def shortMessage(self):
        return self.shortMessage

    def closestPulseDistanceKm(self, roundValue = False):
        if (roundValue == True):
            return round((self.closestPulseDistance * 1.60934), 2)
        else:
            return int(round(self.closestPulseDistance * 1.60934, 0 ))

    def closestPulseDirectionCardinal(self) -> str:
        dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        ix = round(self.closestPulseDirection / (360. / len(dirs)))
        return direction[dirs[ix % len(dirs)]]
        # return ix

    def hasLightningNear(self):
        if int(self.closestPulseDistance) < maxPulseDistance :
            return True
        return False

sites = [ LightningStats(siteName="Sandton", lat=-26.0577, lon=28.0252), # -26.05777099168985, 28.025237442595625
    LightningStats(siteName="West Rand", lat=-26.1414, lon=27.9183),  # -26.141407816350586, 27.918334443436567
    LightningStats(siteName="Kempton Park", lat=-26.0627, lon=28.2280) ] # -26.062777316869795, 28.22805146505124

async def getLocationLightning(lat, lon):
    data = await weatherbug_spark.get_data(lat, lon)
    stats = LightningStats(data.closestPulseDistance, data.closestPulseDirection, data.shortMessage)
    return stats

async def main():
    lightningMessage = ""
    for site in sites:
        data = await weatherbug_spark.get_data(site.lat, site.lon)
        site.closestPulseDistance = data.closestPulseDistance
        site.closestPulseDirection = data.closestPulseDirection
        site.shortMessage = data.shortMessage
        # print(f'Site {site.siteName}: {site.hasLightningNear()} - {site.shortMessage} - {site.closestPulseDistanceKm()}Km - {site.closestPulseDirection} {site.closestPulseDirectionCardinal()}')
        if (site.hasLightningNear()):
            lightningMessage = f'{lightningMessage} {site.closestPulseDistanceKm()} Kilometers {site.closestPulseDirectionCardinal()} from {site.siteName}, '

    if len(lightningMessage) == 0:
        print('No Lightning')
    else:
        print(f'Lightning Warning! {lightningMessage} from Zulu Sierra Nine, Alpha India')

if __name__ == "__main__":
    asyncio.run(main())
