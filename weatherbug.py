import asyncio
import weatherbug_spark
import json
from datetime import datetime
import json
from datetime import datetime

class WeatherBug(object):
    class LightningStats(object): 
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
        
    async def getLightningStrikes(self) -> str: 
        print("WeatherBug Lightning Collector")
        data = await weatherbug_spark.get_data(lat=-26.0577, lon=28.0252)
        stats = WeatherBug.LightningStats(data.closestPulseDistance, data.closestPulseDirection, data.shortMessage)
        dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        ix = round(data.closestPulseDirection / (360. / len(dirs)))
        dt = datetime.now()
        dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")

        jdata = {}
        jdata['datetime'] = dt_str
        jdata['shortMessage'] = data.shortMessage
        jdata['distanceKM'] = round(data.closestPulseDistance * 1.60934, 2)
        jdata['direction'] = dirs[ix % len(dirs)]
        json_data = json.dumps(jdata)

        return json_data