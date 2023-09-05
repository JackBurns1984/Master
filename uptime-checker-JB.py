import requests
import json
import os
import win32com.client as win32
import subprocess
import datetime as datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# function
def sendemail(message, emailto, subject):
    outlook = win32.Dispatch("outlook.application")
    mail = outlook.CreateItem(0)
    mail.To = emailto
    mail.Subject = subject
    mail.Body = message
    mail.Send()

def webcheck(url,filename):
    try:
        rg = requests.get(
            url,
            verify=False,
        )
        if rg.status_code != 200:
            if os.path.isfile(filename):
                breakpoint
            else:
                f = open(filename, "a")
                f.close()
                print("website is active but didnt return status 200")
                emailto = "jack.burns@kennedyslaw.com"
                subject = "CKAN Notification"
                message = "The website " + url + " isnt returning status code 200"
                sendemail(message, emailto, subject)
                breakpoint

    except:
        # We should never hit this.
        print("website is completely down")

webcheck("https://data.kennedyslaw.local",'files/data.txt')
webcheck("https://terms.kennedyslaw.local",'files/terms.txt')
webcheck("https://contracts.kennedyslaw.local",'files/contracts.txt')
webcheck("https://systems.kennedyslaw.local",'files/systems.txt')