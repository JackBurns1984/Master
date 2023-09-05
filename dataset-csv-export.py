import requests
import json
import os
import pandas as pd
import math

# API token for dev
#Token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJ3dmo1ZmVUa2QzbldLSjhPeV9Jb0lXdnlJVFpHb1MtMWo4T3V1YTZrT29JYWxzNDI5UFBFbno3Yl9iLWZUOU00cGFvdEZXNy1HQ1kwRnpTeSIsImlhdCI6MTY3ODQzNjI2N30.OeO76L2c23a_dUqpOP1XA-sPbHf0yW1v18jD3uuy-a0"

# API token for live
Token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJoMXFJZzF2TW1KYXRNamF6NFN4Yk51cGNKZXZ1U0lWczFKbF9HOVZoY1hEU0RNS1Vxczh4TkdoV2tkYlBEczVLZGlmQnVVVndEOTd4YkxrOCIsImlhdCI6MTY4MjA4OTQ2NH0.nTNbqWwC0kp0cxHszaeucXDOBv5QaL8CYGGQW4lzHEI"

# presets
rowdata = []
df = pd.DataFrame(columns=["title",
    "url",
    "name",
    "description",
    "publisher",
    "personal_data",
    "special_cat_data",
    "created",
    "last_updated",
    "next_update_due",
    "update_frequency",
    "accurancy_assessment",
    "precision",
    "geographical_coverage",
    "temporal_granularity",
    "temporal_coverage_from",
    "temporal_coverage_to",
    "linked_data",
    "information_type",
    "type_of_data",
    "taxonomy_url",
    "resources_url",
    "resources_format",
    "no_of_fields",
    "csv_or_txt_provided",
    "owner_org",
    "owned_by",
    "managed_by",
    "contact_email",
    "license_Id",
    "provided_data",
    "shared_data",
    "regulatory_limitations",
    "risk_rag",
    "dataset_classification",
    "other_docs",
    "tag_string",
    "pers",
    "fin",
    "health",
    "gov",
    "size",
    "generated_from"])

# functions
def floatcheck(item):
    try:
        return resultall["result"][item]
    except:
        return ''


rg = requests.get(
    "https://data.kennedyslaw.local/api/3/action/package_list",
    #"http://localhost:5000/api/3/action/package_list",
    verify=False,
)
results = rg.json()
for dataset in results["result"]:
    rowdata = []
    dataset = dataset.replace("&","%26")
    print(dataset)
    # now request all the data in each dataset
    rgall = requests.get(
        "https://data.kennedyslaw.local/api/3/action/package_show?id="+dataset,
        #"http://localhost:5000//api/3/action/package_show?id=" + dataset,
        verify=False,
    )
    resultall = rgall.json()

#checks
    updated = floatcheck('last_updated')
    next_due = floatcheck('next_update_due')
    title = floatcheck('title')
    url = floatcheck('url')
    name = floatcheck('name')
    description = floatcheck('description')
    organization = resultall['result']['organization']['name']
    personal_data = floatcheck('personal_data')
    special_cat_data = floatcheck('special_cat_data')
    created = floatcheck('created')
    update_frequency = floatcheck('update_frequency')
    acc_assesment = floatcheck('accurancy_assessment')
    precision = floatcheck('precision')
    geo_coverage = floatcheck('geographical_coverage')
    temp_gran = floatcheck('temporal_granularity')
    temp_cov_from = floatcheck('temporal_coverage_from')
    temp_cov_to = floatcheck('temporal_coveral_to')
    linked_data = floatcheck('linked_data')
    information_type = floatcheck('information_type')
    type_of_data = floatcheck('type_of_data')
    taxonomy_url = floatcheck('taxonomy_url')
    resources_url = floatcheck('resources_url')
    resources_format = floatcheck('resources_format')
    no_of_fields = floatcheck('no_of_fields')
    csv_or_txt = floatcheck('csv_or_txt_provided')
    owner_org = resultall['result']['organization']['name']
    owned_by = floatcheck('owned_by')    
    managed_by = floatcheck('managed_by')
    contact_email = floatcheck('contact_email')
    license_Id = floatcheck('license_Id')
    provided_data = floatcheck('provided_data')
    shared_data = floatcheck('shared_data')
    regulatory_limitations = floatcheck('regulatory_limitations')
    risk_rag = floatcheck('risk_rag')
    dataset_classification = floatcheck('dataset_classification')
    other_docs = floatcheck('other_docs')
    tag_string = floatcheck('tag_string')
    pers = floatcheck('pers')
    fin = floatcheck('fin')
    health = floatcheck('health')
    gov = floatcheck('gov')
    size = floatcheck('size')
    generated_from = floatcheck('generated_from')


    #now list the group for insertion into df
    grouping = ({
        "title":title,
        "url":url,
        "name":name,
        "description":description,
        "publisher":organization,
        "peronal_data":personal_data,
        "special_cat_data":special_cat_data,
        "created":created,
        "last_updated":updated,
        "next_update_due":next_due,
        "update_frequency":update_frequency,
        "accurancy_assessment":acc_assesment,
        "precision":precision,
        "geographical_coverage":geo_coverage,
        "temporal_granularity":temp_gran,
        "temporal_coverage_from":temp_cov_from,
        "temporal_coverage_to":temp_cov_to,
        "linked_data":linked_data,
        "information_type":information_type,
        "type_of_data":type_of_data,
        "taxonomy_url":taxonomy_url,
        "resources_url":resources_url,
        "resources_format":resources_format,
        "no_of_fields":no_of_fields,
        "csv_or_txt_provided":csv_or_txt,
        "owner_org":owner_org,
        "owned_by":owned_by,
        "managed_by":managed_by,
        "contact_email":contact_email,
        "license_Id":license_Id,
        "provided_data":provided_data,
        "shared_data":shared_data,
        "regulatory_limitations":regulatory_limitations,
        "risk_rag":risk_rag,
        "dataset_classification":dataset_classification,
        "other_docs":other_docs,
        "tag_string":tag_string,
        "pers":pers,
        "fin":fin,
        "health":health,
        "gov":gov,
        "size":size,
        "generated_from":generated_from,
    })


    print(grouping)



    print(df)
    df = df.append(grouping,ignore_index = True)
    print(df)

df.to_csv('df.csv')
