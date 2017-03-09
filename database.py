import MySQLdb
#if not installed: sudo apt-get install python-mysqldb

def get_events(location):

    db=MySQLdb.connect(host="10.0.0.205",port=3306,user="welkom",passwd="eventsopscherm",db="kvkaw")
    cursor=db.cursor()
    
    events = None
    if location == "Antwerpen":
        cursor.execute("SELECT event, DATE_FORMAT(starttijd,'%H:%i'),locatie FROM welkomscherm WHERE vestiging = 'Antwerpen' AND datum = CURDATE() AND eindtijd >= CURTIME() ORDER BY starttijd ASC")
        events = cursor.fetchall()
        count = cursor.rowcount
        #events = "Vooruitblik"
    if location == "Waasland":
        cursor.execute("SELECT event, DATE_FORMAT(starttijd,'%H:%i'),locatie FROM welkomscherm WHERE vestiging = 'Waasland' AND datum = CURDATE() AND eindtijd >= CURTIME() ORDER BY starttijd ASC")
        events = cursor.fetchall()
        count = cursor.rowcount
        #events = "Nieuwsjaarsreceptie"
    return events, count


def get_agenda():

    db=MySQLdb.connect(host="10.0.0.205",port=3306,user="welkom",passwd="eventsopscherm",db="kvkaw")
    cursor=db.cursor()
    
    agenda = None
    cursor.execute("SELECT event, datum FROM kameragenda WHERE datum >= CURDATE() ORDER BY datum ASC LIMIT 3")
    agenda = cursor.fetchall()
    count = cursor.rowcount
    return agenda, count
