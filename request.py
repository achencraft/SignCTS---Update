import requests
import json
from datetime import datetime

class Request:
    def __init__(self,token):
        self.token = token
        self.session = requests.Session()
        self.session.auth = (self.token, "")

  


    def show_next(self,station):
        request = "https://api.cts-strasbourg.eu/v1/siri/2.0/stop-monitoring?MaximumStopVisits=3&MinimumStopVisitsPerLine=1&MonitoringRef="
        request += station
        query = self.session.get(request)
        ans = json.loads(query.text)
        rep = []
        
        if(ans["ServiceDelivery"]["StopMonitoringDelivery"][0]['MonitoringRef'] != None):
        
            for passage in ans["ServiceDelivery"]["StopMonitoringDelivery"][0]['MonitoredStopVisit']:
                line = passage['MonitoredVehicleJourney']['PublishedLineName']
                destination = passage['MonitoredVehicleJourney']['DestinationName']
                heure_passage = passage['MonitoredVehicleJourney']['MonitoredCall']['ExpectedDepartureTime']
                temps = Time_convert(heure_passage)
                now = datetime.now()
                diff = temps - now
                temps_attente = str(diff.seconds//60)

                rep.append([line,destination,temps_attente])
        
  

        
        return rep[:3]
        

    def show_station_list(self):
        query = self.session.get("https://api.cts-strasbourg.eu/v1/siri/2.0/stoppoints-discovery")
        ans = json.loads(query.text)
        nbr_arret = len(ans["StopPointsDelivery"]["AnnotatedStopPointRef"])
        
        msg = ""
        for i in range (0,nbr_arret):
            msg += ans["StopPointsDelivery"]["AnnotatedStopPointRef"][i]["StopName"] + "\n"

    
def Time_convert(temps):
    arr = temps.split('T')
    arr_date = arr[0].split('-')
    arr_bis = arr[1].split('+')
    arr_hour = arr_bis[0].split(':')

    return datetime(int(arr_date[0]),int(arr_date[1]), int(arr_date[2]), int(arr_hour[0]), int(arr_hour[1]), int(arr_hour[2]))
