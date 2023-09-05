import requests
from bs4 import BeautifulSoup
import pandas as pd

urllist = []
urllist += ["https://www.lloyds.com/help/glossary-and-acronyms/"]


iterlist = 0
df = pd.DataFrame()

for url in urllist:
    page = requests.get(
        url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    soup = BeautifulSoup(
        page.content, "html.parser"
    )  # Parsing content using beautifulsoup

    print(soup)

    soup = soup.find_all("div", class_="container glorrary-terms")

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
df.to_csv("ckan/scraped-data/lloyds-scraped.csv")
