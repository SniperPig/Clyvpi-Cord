import sqlite3
from datetime import datetime

con = sqlite3.connect('ClyvpiDatabase.db', detect_types=sqlite3.PARSE_DECLTYPES)


def rfidInstance(rfid):
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
    cur = con.cursor()
    print("I am here")
    cur.execute("SELECT FullName FROM User WHERE rfid = :rfid", {"rfid": rfid})
    return cur.fetchall()