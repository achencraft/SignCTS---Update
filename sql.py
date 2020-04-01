import mysql.connector


class SQL:
    def __init__(self,hostname, port, db_name, username, password):
        self.hostname = hostname
        self.port = port
        self.db_name = db_name
        self.username = username
        self.password = password


    def getStopList(self):
        rep = []

        mydb = mysql.connector.connect(
            host=self.hostname,
            user=self.username,
            passwd=self.password,
            database=self.db_name
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT DISTINCT IDSAE FROM signcts")
        myresult = mycursor.fetchall()

        for ans in myresult:   
            rep.append(ans[0])
        
        rep.remove('TimeStamp')
        return rep

    def updateData(self, values):
        mydb = mysql.connector.connect(
            host=self.hostname,
            user=self.username,
            passwd=self.password,
            database=self.db_name
        )

        #insertion horaires
        mycursor = mydb.cursor()

        sql = "UPDATE signcts SET LIGNE=%s, DESTINATION=%s, HORAIRE=%s WHERE IDSAE=%s AND Numero=%s"
        mycursor.executemany(sql, values[:-1])
        mydb.commit()

        #insertion timestamp

        mycursor = mydb.cursor()

        sql = "UPDATE signcts SET LIGNE=%s, DESTINATION=%s, HORAIRE=%s WHERE IDSAE=%s"
        mycursor.execute(sql, values[-1])
        mydb.commit()

  