import MySQLdb #if not installed: sudo apt-get install python-mysqldb
import json
# -*- coding: utf-8 -*-

def DB_conn():

    with open ('/home/pi/Desktop/welkomscherm_conf.json','r') as cfg:
        config = json.load(cfg)

    host= config['DB']['host']
    user= config['DB']['user']
    passwd= config['DB']['passwd']
    db= config['DB']['db']

    db=MySQLdb.connect(host,user,passwd,dbcharset='utf8',use_unicode=True)
    cursor=db.cursor()
    return cursor

def get_events(location,detail):

    cursor = DB_conn()
    events = None
    if location == "Antwerpen" and detail !="Auditorium":
        cursor.execute("SELECT event, DATE_FORMAT(starttijd,'%H:%i'),locatie FROM welkomscherm WHERE vestiging = 'Antwerpen' AND datum = CURDATE() AND eindtijd >= CURTIME() ORDER BY starttijd ASC")
        events = cursor.fetchall()
        count = cursor.rowcount
    if location == "Waasland"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                :
        cursor.execute("SELECT event, DATE_FORMAT(starttijd,'%H:%i'),locatie FROM welkomscherm WHERE vestiging = 'Waasland' AND datum = CURDATE() AND eindtijd >= CURTIME() ORDER BY starttijd ASC")
        events = cursor.fetchall()
        count = cursor.rowcount
    if location == "Antwerpen" and detail == "Auditorium":
        cursor.execute("SELECT event, DATE_FORMAT(starttijd,'%H:%i'),locatie FROM welkomscherm WHERE locatie like '%auditorium%' AND datum = CURDATE() AND eindtijd >= CURTIME() ORDER BY starttijd ASC")
        events = cursor.fetchall()
        count = cursor.rowcount
    return events, count


def get_agenda():

    cursor= DB_conn()
    agenda = None
    cursor.execute("SELECT event, DATE_FORMAT(datum,'%d %M '), type FROM kameragenda WHERE datum >= CURDATE() ORDER BY datum ASC LIMIT 3")
    agenda = cursor.fetchall()
    count = cursor.rowcount
    return agenda, count

