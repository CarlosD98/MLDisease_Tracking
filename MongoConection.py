from pymongo import MongoClient

import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import requests
import json
from sklearn.linear_model import LinearRegression


diseases = requests.get('http://54.211.232.101:8080/api/diseases/')


for i in diseases.json():
    print(i)

    cursor = requests.get("http://localhost:8080/api/diseases/report/"+i)
    print(cursor)
    l = list(cursor.json())

    df = pd.DataFrame(l)
    print(df.head())
    df['date'] = pd.to_datetime(df['date'])
    X = df["date"].map(dt.datetime.toordinal)

    x = X.values.reshape(-1, 1)

    model = LinearRegression()
    model.fit(x, df['cases'])  # train the model

    start = df["date"].max() - dt.timedelta(days=10)
    print(start)
    datelist = pd.date_range(start.strftime("%d-%m-%Y"), end=dt.datetime.today() + dt.timedelta(days=30))

    X_test = datelist.map(dt.datetime.toordinal)
    x_test = X_test.values.reshape(-1, 1)
    y_predict = model.predict(x_test)
    my_dates = []
    print(type(my_dates))
    forecast = pd.DataFrame()
    forecast['cases'] = list(y_predict)

    for j in x_test:
        d = dt.date.fromordinal(j[0]).strftime('%Y-%m-%d')
        my_dates.append(d)
    forecast['dates'] = my_dates
    fc = forecast.to_numpy()

    dates = []
    for d in df['date']:
        print(type(d))
        temp = d.to_pydatetime()
        dates.append(temp.strftime('%Y-%m-%d'))
    df['dates'] = dates
    del df['date']
    data = df.to_numpy()
    lData = data.tolist()

    body = json.dumps({"disease": i, "date": dt.date.today().strftime('%Y-%m-%d'),
                       "forecast": fc.tolist(), "data": lData[::-1]})
    print(body)
    #req = requests.post("http://localhost:8080/forecast", body)
   # print(req.json())
    print(model.intercept_, model.coef_)

# plt.plot(datelist, y_predict, color='red', linewidth=2)

# plt.show()
