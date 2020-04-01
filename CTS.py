from request import *
from sql import *
import datetime
import schedule
import time

######################## DONNEES ##############################

#TOKEN CTS
TOKEN = 'INSERT_TOKEN_HERE'

#SQL
HOSTNAME = "localhost"
PORT = 3306
DB_NAME = 'INSERT_HERE'
USERNAME = "INSERT_HERE"
PASSWORD = "INSERT_HERE"


###############################################################


def signCts():
    print("fct")
    #get list of stops to query
    sql = SQL(HOSTNAME, PORT, DB_NAME, USERNAME, PASSWORD)
    StopList = sql.getStopList()


    req = Request(TOKEN)
    AllData = []

    #get data from webservice
    for stop in StopList:
        retour = [stop]
        req.show_next(stop)
        retour.append(req.show_next(stop))
        AllData.append(retour)


    #insert datas to database

    ArgumentsQuery = []

    date_actuelle = datetime.datetime.now()

    for stop in AllData:
        idsae = stop[0]
        passages = stop[1]
        nbr_passage = len(passages)

        for i in range(3):

            
            if(i < nbr_passage):
                
                ArgumentsQuery.append((passages[i][0],passages[i][1],passages[i][2],idsae,i))

            else:

                ArgumentsQuery.append(('','',-1,idsae,i))



    ArgumentsQuery.append((str(date_actuelle),'',-1,'TimeStamp'))


    sql.updateData(ArgumentsQuery)



schedule.every(0.2).minutes.do(signCts)

while 1:
    schedule.run_pending()