import requests
import json
from datetime import datetime

class Request:
    def __init__(self,token):
        self.token = token
        self.session = requests.Session()
        self.session.auth = (self.token, "")

  


    def show_next(self,StopsList):
        request = "https://api.cts-strasbourg.eu/v1/siri/2.0/stop-monitoring?MaximumStopVisits=3&MinimumStopVisitsPerLine=1"
        rep = []
        index = []

        for stop in StopsList:
            request += "&MonitoringRef=" + stop
            rep.append([stop,[]])
            index.append(stop)


        query = self.session.get(request)
        ans = json.loads(query.text)


    
        

        
        if(ans["ServiceDelivery"]["StopMonitoringDelivery"][0]['MonitoringRef'] != None):
        
            for passage in ans["ServiceDelivery"]["StopMonitoringDelivery"][0]['MonitoredStopVisit']:
                IDSAE = passage['MonitoringRef']
                line = passage['MonitoredVehicleJourney']['PublishedLineName']
                destination = passage['MonitoredVehicleJourney']['DestinationName']
                heure_passage = passage['MonitoredVehicleJourney']['MonitoredCall']['ExpectedDepartureTime']
                temps = Time_convert(heure_passage)
                now = datetime.now()
                diff = temps - now
                temps_attente = str(diff.seconds//60)

                index_stop = index.index(IDSAE)

                if(len(rep[index_stop][1]) < 3):
                    rep[index_stop][1].append([line,destination,temps_attente])
        
  

        return rep
        

    
def Time_convert(temps):
    arr = temps.split('T')
    arr_date = arr[0].split('-')
    arr_bis = arr[1].split('+')
    arr_hour = arr_bis[0].split(':')

    return datetime(int(arr_date[0]),int(arr_date[1]), int(arr_date[2]), int(arr_hour[0]), int(arr_hour[1]), int(arr_hour[2]))
