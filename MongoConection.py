from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import requests
from sklearn.linear_model import LinearRegression

diseases = requests.get('http://54.211.232.101:8080/api/')
mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % ('carlos', 'carlos123', 'localhost', '27017', 'testdb')
client = MongoClient(mongo_uri)
db = client["testdb"]
forecast = db['forecast']
for i in diseases.json():
    print(i)

    cursor = db.case.aggregate([{"$match":{'disease': i}},{"$group": {"_id": "$date", "cases":{"$sum":1}}}])

    df = pd.DataFrame(list(cursor))
    df.plot(x='_id', y='cases')
    X = df["_id"].map(dt.datetime.toordinal)

    x = X.values.reshape(-1, 1)

    plt.title('Disease track')
    plt.xlabel('Date')
    plt.ylabel('Cases')

    model = LinearRegression()
    model.fit(x, df['cases'])  # train the model

    start = df["_id"].max()-dt.timedelta(days=10)
    print(start)
    datelist = pd.date_range(start.strftime("%d-%m-%Y"), end=dt.datetime.today()+dt.timedelta(days=30))

    X_test = datelist.map(dt.datetime.toordinal)
    x_test = X_test.values.reshape(-1, 1)
    y_predict = model.predict(x_test)
    my_dates = {}
    for i, val in enumerate(x_test):
        d = dt.date.fromordinal(val[0]).strftime('%Y-%m-%d')
        my_dates[d] = y_predict[i]

    print(my_dates)
    forecast.insert_one({"Test": my_dates})

print(model.intercept_, model.coef_)

plt.plot(datelist, y_predict, color='red', linewidth=2)

#plt.show()