import requests
import json

def notify(name): 
    payload = {'name': name }
    r = requests.post('http://videosurv-906.appspot.com/identify', data=payload)
    return r.text
