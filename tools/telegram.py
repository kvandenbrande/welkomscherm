import os, json

def send_telegram(MESSAGE):
    try:
        with open('/home/pi/Desktop/welkomscherm_conf.json', 'r') as f:
            config = json.load(f)
    except ValueError:
        print ('Error: Decoding config has failed')

    TELEGRAM_TOKEN = config['TELEGRAM']['token']
    TELEGRAM_CHAT_ID = config['TELEGRAM']['chatID']

    string = "curl -s -X POST https://api.telegram.org/bot"+TELEGRAM_TOKEN+"/sendMessage -d chat_id="+TELEGRAM_CHAT_ID+" -d text=\""+MESSAGE+"\""
    print (string)
    os.system(string)
    return 0

