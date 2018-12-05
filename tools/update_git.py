#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import os, time
from bs4 import BeautifulSoup
from telegram import send_telegram

def get_github_commit(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    commit = soup.find('span', {'class' : 'num text-emphasized'})
    commit = commit.get_text() 
    remote_commit = int(commit)
    return remote_commit


def write_commit(commit):
    try:
        with open('/home/pi/Desktop/welkomscherm_conf.json', 'r') as f:
            config = json.load(f)
    except ValueError:
        print ('Error: Decoding config has failed')

    config['GITHUB']['commit'] = commit

    with open('/home/pi/Desktop/welkomscherm_conf.json', 'w') as f:
        json.dump(config, f)


def main():
    try:
        with open('/home/pi/Desktop/welkomscherm_conf.json', 'r') as f:
            config = json.load(f)
    except ValueError:
        print ('Error: Decoding config has failed')

    LOCATION = config['LOCATION']['vestiging']
    LOCATION_DETAIL = config['LOCATION']['locatie']
    GITHUB_URL = config['GITHUB']['url']
    CURRENT_COMMIT = config['GITHUB']['commit']

    remote_commit = get_github_commit(GITHUB_URL)
    
    if remote_commit == CURRENT_COMMIT:
        print ("Everything up-to-date")
    else:
        CMD = "sudo rm -rf /home/pi/welkomscherm && cd /home/pi && "+"git clone "+ GITHUB_URL +".git"+" && chmod +x /home/pi/welkomscherm/welkomscherm.py && sudo reboot"
        print (CMD)
        write_commit(remote_commit)
        message= LOCATION +" - "+LOCATION_DETAIL + " will get it's update now"
        send_telegram(message)
        os.system (CMD)
        


if __name__ == "__main__":
    main()


