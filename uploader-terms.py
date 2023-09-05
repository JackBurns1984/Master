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


# website
url = "https://terms.kennedyslaw.local/api/3/action/package_create"

# API token is unique per user and site.
Token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJ3aHlWbUhRalJrOXloZkFiSElUSTFObGVSbG9LZmVGMlhfR3hZU0VEX0tpYk96ZDhhbzZtT0lJYURZMkNwQllaZmtQNlFnMEx4UXBGeHBaUyIsImlhdCI6MTY4MzEyMjY1MX0.rvXb8W_7u6LCTxVlZP6_ywtHJCcX5ds5EndR1A6Fiuo"
file_name = "Insurance Terms.xlsx"

df = pd.read_excel(file_name, header=[0])

# remove the blanks and change them to TBC.
df = df.fillna("TBC")

# cycle through to upload 1 at a time - line 1 is the headers required.
for row in df.itertuples():
    # Ignore row 1 - this is helptext and not required for the upload
    if row.Term == "TBC":
        next
    else:
        Term = floatcheck(row.Term)
        Name = floatcheck(row.Name)
        Acronym = floatcheck(row.Acronym)
        Definition = floatcheck(row.Definition)
        Dictionary = floatcheck(row.Dictionary)
        Dateagreed = checkdate(row._8)
        Publisher = floatcheck(row.Publisher)
        Version = floatcheck(row.Version)
        Source = floatcheck(row.Source)
        Usage = floatcheck(row.Usage)
        Validops = floatcheck(row._16)
        owner = floatcheck(row._17)
        Author = floatcheck(row.Author)
        Originator = floatcheck(row.Originator)
        synonyms_parent = floatcheckblank(row._12)
        synonyms_parent_name = synonyms_parent
        synonyms_child = floatcheckblank(row._13)
        synonyms = floatcheckblank(row.Synonyms)
        TermManager = floatcheck(row._20)
        DictionaryManager = floatcheck(row._21)

        # print(tags)
        Name = Name.lower()
        Publisher = Publisher.replace(" ", "-").lower()
        Source = Source.lower()
        
        # Do the below in the front end so we dont change data
        #if synonyms_parent != "":
        #    Usage = "See Parent Term"
        #    Validops = "See Parent Term"
        #    owner = "See Parent Term"
        #    TermManager = "See Parent Term"
        #    DictionaryManager = "See Parent Term"

        # Put the details of the dataset we're going to create into a dict.
        data = {
            "term": Term,
            "name": Term,
            "acronym": Acronym,
            "definition": Definition,
            "date-approved": Dateagreed,
            "owner_org": Publisher,
            "version": Version,
            "source": Source,
            "usage": Usage,
            "valid_operations": Validops,
            "term_owner": owner,
            "author": Author,
            "originator": Originator,
            "synonyms_parent": synonyms_parent,
            "synonyms_parent_name": synonyms_parent_name,
            "link_child": synonyms_child,
            "synonyms": synonyms,
            "term_manager": TermManager,
            "dictionary_manager": DictionaryManager,
        }
        print("")
        print(data)
        print("")
        # check if owner_org(the publisher) is already in the DB,  if not - add it before uploading.
        rg = requests.get(
            "https://terms.kennedyslaw.local/api/3/action/organization_list",
            verify=False,
        )
        results = rg.json()
        # print(ownedby)
        # print(owner)
        # print(row.Title)
        if Publisher not in (results["result"]):
            # print("new owner")
            ownerdata = {"name": Publisher}
            ro = requests.post(
                "https://terms.kennedyslaw.local/api/3/action/organization_create",
                ownerdata,
                headers={"Authorization": Token},
                verify=False,
            )
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
