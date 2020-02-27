from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from sklearn import metrics
from sklearn.linear_model import LinearRegression

mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % ('carlos', 'carlos123', 'localhost', '27017', 'testdb')
client = MongoClient(mongo_uri)
db = client["testdb"]

cursor = db.case.aggregate([{"$match":{'disease': "COVID_19"}},{"$group": {"_id": "$date", "cases":{"$sum":1}}}])

df = pd.DataFrame(list(cursor))

print(df.head())
df.plot(x='_id', y='new cases')
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

print(model.intercept_, model.coef_)

plt.plot(datelist, y_predict, color='red', linewidth=2)

plt.show()