import xlrd as xr
import requests as req
import json


url = "http://54.211.232.101:8080/case"
wb = xr.open_workbook('cleanDS.xlsx')
sheet = wb.sheet_by_index(1)
nx = 0
print("Start")
for n in range(0, sheet.ncols):
    for cell in sheet.col(n):
        j = json.loads(cell.value)
        x = j['rep']
        del j['rep']
        j['firstName'] = j['firstname']
        del j['firstname']
        j['lastName'] = j['lastname']
        del j['lastname']
        for i in range(0, x):
            req.post(url, json=j)
            nx += 1

print(nx)


