import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import datetime as dt

df = pd.read_csv('time_series_2019_ncov_confirmed.csv')
df.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], inplace=True, axis=1)  # remove unnecessary Columns
ds = df.sum(axis=0, skipna=True)  # Sum each column cases
ds = pd.DataFrame(ds)
d = {"Date": ds.index, "Cases": ds[0]}
data = pd.DataFrame(data=d)
data.reset_index(drop=True, inplace=True)
data["Date"] = pd.to_datetime(data['Date'])

print(data.head())


data.plot(x='Date', y='Cases', style='o')
X = data["Date"].map(dt.datetime.toordinal)
x = X.values.reshape(-1,1)
plt.title('Disease growth')
plt.xlabel('Date')
plt.ylabel('Cases')

model = LinearRegression()
model.fit(x, data['Cases'])  # train the model
y_pred = model.predict(x)
plt.plot(x,y_pred, color='red', linewidth=2)
plt.show()

plt.show()