import requests
from bs4 import BeautifulSoup
import pandas as pd

urllist = []
urllist += [
    "https://www.abi.org.uk/data-and-resources/tools-and-resources/glossary/?p=1"
]
urllist += [
    "https://www.abi.org.uk/data-and-resources/tools-and-resources/glossary/?p=2"
]
urllist += [
    "https://www.abi.org.uk/data-and-resources/tools-and-resources/glossary/?p=3"
]

iterlist = 0
df = pd.DataFrame()

for url in urllist:
    page = requests.get(url)
    soup = BeautifulSoup(
        page.content, "html.parser"
    )  # Parsing content using beautifulsoup

    soup = soup.find_all("div", class_="page-list__main")

    print(soup[0].text)

    rendered = soup[0].text.split("\r")
    for row in rendered:
        print(row)
        try:
            data = row.split("\n")
            title = data[1]
            desc = data[2]
            adddata = {"title": title, "Description": desc}
            df = df.append(adddata, ignore_index=True)
        except:
            print("not a valid row")
print(df)
# df.to_csv("abi-scraped"+str(iterlist)+".csv")
df.to_csv("ckan/scraped-data/abi-scraped.csv")
