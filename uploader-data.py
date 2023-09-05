import requests
import json
import os
import pandas as pd
import math


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


# converts the data for encryption tables.
def ency(rest, trans, mob):
    ans = []
    if rest == "Yes":
        ans += ["rest"]
    elif rest == "No":
        ans += ["not-rest"]
    if trans == "Yes":
        ans += ["transit"]
    elif trans == "No":
        ans += ["not-transit"]
    if mob == "Yes":
        ans += ["mobile"]
    elif mob == "No":
        ans += ["not-mobile"]
    if ans == "":
        return "TBC"
    else:
        return ans


# live api
url = "https://data.kennedyslaw.local/api/3/action/package_create"
# dev api
# url = "http://localhost:5000/api/3/action/package_create"

# API token for dev
#Token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJ3dmo1ZmVUa2QzbldLSjhPeV9Jb0lXdnlJVFpHb1MtMWo4T3V1YTZrT29JYWxzNDI5UFBFbno3Yl9iLWZUOU00cGFvdEZXNy1HQ1kwRnpTeSIsImlhdCI6MTY3ODQzNjI2N30.OeO76L2c23a_dUqpOP1XA-sPbHf0yW1v18jD3uuy-a0"

# API token for live
Token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJoMXFJZzF2TW1KYXRNamF6NFN4Yk51cGNKZXZ1U0lWczFKbF9HOVZoY1hEU0RNS1Vxczh4TkdoV2tkYlBEczVLZGlmQnVVVndEOTd4YkxrOCIsImlhdCI6MTY4MjA4OTQ2NH0.nTNbqWwC0kp0cxHszaeucXDOBv5QaL8CYGGQW4lzHEI"
file_name = "Kennedys metadata proforma.xlsx"

df = pd.read_excel(file_name, header=[3])

# remove the blanks and change them to TBC.
df = df.fillna("TBC")

# cycle through to upload 1 at a time - line 1 is the headers required.
for row in df.itertuples():
    # Ignore row 1 - this is helptext and not required for the upload
    if row.Index < 1 or row.Title == "TBC":
        next
    else:
        # date checks and formatting
        createddate = checkdate(row._8)
        lastupdatedate = checkdate(row._9)
        nextupdatedate = checkdate(row._10)
        tempfrom = checkdate(row._16)
        tempto = checkdate(row._17)

        # empty data checks - converts from nan to None
        granularity = floatcheck(row._15)
        classification = floatcheck(row._35)
        riskrag = floatcheck(row._34)
        infotype = floatcheck(row._19)
        datatype = floatcheck(row._20)
        updatefreq = floatcheck(row._11)
        accuracy = floatcheck(row._12)
        geocover = floatcheck(row._14)
        publisher = floatcheck(row.Publisher)
        linkurl = floatcheck(row.URL)
        personaldata = floatcheck(row._6)
        specialdata = floatcheck(row._7)
        precision = floatcheck(row.Precision)
        taxurl = floatcheck(row._21)
        resourceurl = floatcheck(row._22)
        resourceformat = floatcheck(row._23)
        numfields = floatcheck(row._25)
        csvprovided = floatcheck(row._26)
        ownedby = floatcheck(row._27)
        managedby = floatcheck(row._28)
        email = floatcheck(row._29)
        licenceid = floatcheck(row._30)
        provideddata = floatcheck(row._31)
        shareddata = floatcheck(row._32)
        regulatorylimits = floatcheck(row._33)
        otherdocs = floatcheck(row._36)
        generatefrom = floatcheck(row._51)

        # refactor tags to a list - helps the custom tag section to follow.
        tags = []
        # if row.Tags != None:
        #    tagstring = row.Tags.split(",")
        #    for tagitem in tagstring:
        #        tags += [tagitem]

        # for encryption, upload each block into 1 attribute list.
        pers = ency(row._38, row._39, row._40)
        fin = ency(row._41, row._42, row._43)
        health = ency(row._44, row._45, row._46)
        gov = ency(row._47, row._48, row._49)
        size = floatcheck(row._50)

        # Auto Tagging
        # print(tags)
        if tags == None or tags == "TBC":
            tags = []
        if personaldata == "Yes":
            tags += ["Personal Data"]
        if specialdata == "Yes":
            tags += ["Special Category Data"]

        print(tags)
        owner = publisher.replace(" ", "-").lower()
        name = row.Title.replace(" ", "-").lower()
        print(name)
        if riskrag == 1:
            riskrag = 'one'
        elif riskrag == 2:
            riskrag = 'two'
        elif riskrag == 3:
            riskrag = 'three'
        elif riskrag == 4:
            riskrag = 'four'
        elif riskrag == 6:
            riskrag = 'six'
        elif riskrag == 9:
            riskrag = 'nine'
        else:
            riskrag = 'TBC'

        # Put the details of the dataset we're going to create into a dict.
        data = {
            "title": row.Title,
            "url": linkurl,
            "name": row.Title,
            "description": row.Description,
            "publisher": publisher,
            "personal_data": personaldata,
            "special_cat_data": specialdata,
            "created": createddate,
            "last_updated": lastupdatedate,
            "next_update_due": nextupdatedate,
            "update_frequency": updatefreq,
            "accurancy_assessment": accuracy,
            "precision": precision,
            "geographical_coverage": geocover,
            "temporal_granularity": granularity,
            "temporal_coverage_from": tempfrom,
            "temporal_coverage_to": tempto,
            "linked_data": linkurl,
            "information_type": infotype,
            "type_of_data": datatype,
            "taxonomy_url": taxurl,
            "resources_url": resourceurl,
            "resources_format": resourceformat,
            "no_of_fields": numfields,
            "csv_or_txt_provided": csvprovided,
            "owner_org": owner,
            "owned_by": ownedby,
            "managed_by": managedby,
            "contact_email": email,
            "license_Id": licenceid,
            "provided_data": provideddata,
            "shared_data": shareddata,
            "regulatory_limitations": regulatorylimits,
            "risk_rag": riskrag,
            "dataset_classification": classification,
            "other_docs": otherdocs,
            "tag_string": tags,
            "pers": pers,
            "fin": fin,
            "health": health,
            "gov": gov,
            "size": size,
            "generated_from": generatefrom,
        }
        print("")
        print(data)
        print("")
        # check if owner_org(the publisher) is already in the DB,  if not - add it before uploading.
        rg = requests.get(
            "https://data.kennedyslaw.local/api/3/action/organization_list",
            #"http://localhost:5000/api/3/action/organization_list",
            verify=False,
        )
        results = rg.json()
        # print(ownedby)
        # print(owner)
        # print(row.Title)
        if owner not in (results["result"]):
            # print("new owner")
            ownerdata = {"name": owner, "display_name": publisher}
            ro = requests.post(
                "https://data.kennedyslaw.local/api/3/action/organization_create",
                #"http://localhost:5000/api/3/action/organization_create",
                ownerdata,
                headers={"Authorization": Token},
                verify=False,
            )
            print(ro.text)

        # now post the full data
        r = requests.post(url, data, headers={"Authorization": Token}, verify=False)

        print("Now the output")
        print(r.text)
        if r.status_code != 200:
            print("error")
