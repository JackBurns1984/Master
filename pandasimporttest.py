import pandas as pd
import os

file_name = "Insurance Terms & Jargon.xlsx"

df = pd.read_excel(file_name, sheet_name=None)

print(df)

print("Done")
