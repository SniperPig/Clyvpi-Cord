import sqlite3
from datetime import datetime

# Establishes the database connection.
con = sqlite3.connect('ClyvpiDatabase.db', detect_types=sqlite3.PARSE_DECLTYPES)


def rfidInstance(rfid):
    """
    Adds a RFID into the database with the current datetime.
    :param rfid: the desired RFID
    :type rfid: int
    """
    print("Starting rfid DB insert")
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Date: " + dt_string)
    cur = con.cursor()
    cur.execute("INSERT INTO rfidlogin(rfid, scan_date) values(?, ?)", (rfid, dt_string))
    con.commit()
    print("Finished rfid DB insert")



def getUserByRfid(rfid):
    """
    Gets a user from the database by their RFID tag number.
    :param rfid: the desired RFID
    :type rfid: int
    :return: a user
    :rtype: str
    """
    cur = con.cursor()
    print("I am here")
    cur.execute("SELECT FullName FROM User WHERE rfid = :rfid", {"rfid": rfid})
    return cur.fetchall()



def getThresoldByRfid(rfid):
    cur = con.cursor()
    print("I am here")
    cur.execute("SELECT threshold_light, threshold_temp FROM threshold WHERE rfid = :rfid", {"rfid": rfid})
    return cur.fetchall()

def updateThresholdLight(rfid):
    cur = con.cursor()
    cur.execute("UPDATE threshold SET threshold_light = :threshold_light WHERE rfid = :rfid", {"rfid": rfid})
    return cur.fetchall()

def updateThresholdTemp(rfid):
    cur = con.cursor()
    cur.execute("UPDATE threshold SET threshold_temp = :threshold_temp WHERE rfid = :rfid", {"rfid": rfid})
    return cur.fetchall()
