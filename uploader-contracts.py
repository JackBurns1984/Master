import requests
import json
import os
import pandas as pd
import math
import re


# functions

# Checkdate puts date into the correct order for the web - YYYY-MM-DD
def checkdate(rowno):
    try:
        return str(rowno.year) + "-" + str(rowno.month) + "-" + str(rowno.day)
    except:
        return ""


# make sure we have no blanks - blanks should be converted to TBC.
def floatcheck(rowno):
    if rowno == None:
        return "TBC"
    else:
        return rowno


# not in use - might be in the future
def floatcheckblank(rowno):
    if rowno == "TBC":
        return ""


# website
url = "https://contracts.kennedyslaw.local/api/3/action/package_create"
# dev api
#url = "http://localhost:5000/api/3/action/package_create"

# API token is unique per user and site.
#live
Token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJWbVJtWEthZWxfbGxDa1dyckJSdG4yaXZ1bHJaNnZUM2owVHo5ZGRrSG9GM0l0ZUJNSHBZN25FdmFSbEp5U1ZDaUJoSndnRHF3QnNwM2dTbyIsImlhdCI6MTY4NzE1OTQxN30.zSWGXiHWCwf1XsFFMXbtHAsJxchLIhVr4TMZyiZ4Bk4"
#dev
#Token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJPWGlObUJsQ1hydHljbzk4cE9EYlNiNVNsQXRoeWJKc3ZLNUFJaWlsVl8wVE8xb1JycklDNVBHaTBPVkkzcVVzMlpiS1hEVC1tMTM4V2NUNyIsImlhdCI6MTY4NjgzNjE1M30.ETUD5TWzbHb1-n5pLI6UoO5C0iZe3MdmXvNEWP_A98A"
file_name = "Kennedys Master Supplier Log.xlsx"

df = pd.read_excel(file_name, header=[7])

# remove the blanks and change them to TBC.
df = df.fillna("TBC")

# cycle through to upload 1 at a time - line 1 is the headers required.
for row in df.itertuples():
    # Ignore row 1 - this is helptext and not required for the upload
    if row._2 == "TBC":
        next
    else:
        name = floatcheck(row.Supplier).title()
        owner_org = floatcheck(row.Supplier)
        owner = owner_org.replace(" ", "-").lower()
        owner, n = re.subn('[^A-Za-z0-9]+', '', owner)

        if floatcheck(row._5) == 'Key Supplier':
            supplier_type = 'Key Supplier'
        elif floatcheck(row._5) == 'Preferred Supplier':
            supplier_type = 'Preferred'
        else:
            supplier_type = 'TBC'   
        category = floatcheck(row.Category)
        category, n = re.subn('[^A-Za-z0-9]+', ' ', category)
        sub_category = floatcheck(row._7)
        supplier_relationship = floatcheck(row._8)
        contract_start = checkdate(row._14)
        contract_end = checkdate(row._15)
        if floatcheck(row._16) == 'Yes':
            rolling_contract = 'True'
        else:
            rolling_contract = 'False'

        environmental_risk = floatcheck(row._19)
        csr_risk = floatcheck(row._20)
        information_security_risk = floatcheck(row._21)
        supplier_coverage = floatcheck(row._22) 
        coverageuk = []
        coverageglobal = []
        if supplier_coverage == "UK":
            if floatcheck(row._23) != "TBC":
                coverageuk += floatcheck(row._23)
            if floatcheck(row._24) != "TBC":
                coverageuk += floatcheck(row._24)
            if floatcheck(row._25) != "TBC":
             coverageuk += floatcheck(row._25)
            if floatcheck(row._26) != "TBC":
                coverageuk += floatcheck(row._26)    
            coverageuk = coverageuk.replace(" ", "").lower()  
        elif supplier_coverage == "Global":
            if floatcheck(row._23) != "TBC":
                coverageglobal += floatcheck(row._23)
            if floatcheck(row._24) != "TBC":
                coverageglobal += floatcheck(row._24)
            if floatcheck(row._25) != "TBC":
             coverageglobal += floatcheck(row._25)
            if floatcheck(row._26) != "TBC":
                coverageglobal += floatcheck(row._26)      
            coverageglobal = coverageglobal.replace(" ", "").lower()  

        carbon_emissions = floatcheck(row._27)
        tags = "Active"
        description = ''

        data = {
            "name": name,
            "description": description,
            #"supplier": owner_org,
            "owner_org": owner,
            "supplier_type": supplier_type,
            "category": category,
            "sub_category": sub_category,
            "supplier_relationship": supplier_relationship,
            "contract_start": contract_start,
            "contract_end": contract_end,
            "rolling_contract": rolling_contract,
            "environmental_risk": environmental_risk,
            "csr_risk": csr_risk,
            "information_security_risk": information_security_risk,
            "coverageuk": coverageuk,
            "coverageglobal": coverageglobal,
            "carbon_emissions": carbon_emissions,
            "status":tags,
        }
        print("")
        print(data)
        print("")
        # check if owner_org(the publisher) is already in the DB,  if not - add it before uploading.
        #live
        rg = requests.get(
            "https://contracts.kennedyslaw.local/api/3/action/organization_list",
            verify=False,
        )
        #dev
        #rg = requests.get(
        #    "http://localhost:5000/api/3/action/organization_list",
        #    verify=False,
        #)


        results = rg.json()
        # print(ownedby)
        # print(owner)
        # print(row.Title)
        if owner not in (results["result"]):
            # print("new owner")
            ownerdata = {"name": owner,
                         "title":owner_org.title()}
            #live
            ro = requests.post(
                "https://contracts.kennedyslaw.local/api/3/action/organization_create",
                ownerdata,
                headers={"Authorization": Token},
                verify=False,
            )
            #dev
            #ro = requests.post(
            #    "http://localhost:5000/api/3/action/organization_create",
            #    ownerdata,
            #    headers={"Authorization": Token},
            #    verify=False,
            #)
            print(ro.text)

        # now post the full data
        r = requests.post(
            url,
            data,
            headers={"Authorization": Token},
            verify=False,
        )

        print("Now the output")
        print(r.text)
        if r.status_code != 200:
            print("error")
