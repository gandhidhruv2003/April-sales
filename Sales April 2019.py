import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter
df = pd.read_csv("C:\\Users\\Dhruv Gandhi\\Desktop\\Python\\Sales_Data\\Sales_April_2019.csv")
df = df.replace({
            "Order ID" : "Order ID",
            "Product" : "Product",
            "Quantity Ordered" : "Quantity Ordered",
            "Price Each" : "Price Each",
            "Order Date" : "Order Date",
            "Purchase Address" : "Purchase Address"
}, np.nan)
df.dropna(axis=0,inplace=True)
df["Quantity Ordered"] = pd.to_numeric(df["Quantity Ordered"])      #make int
df["Price Each"] = pd.to_numeric(df["Price Each"])      #make float
df["Sales"] = df["Quantity Ordered"] * df["Price Each"]
df["Date"] = df["Order Date"].str[3:5]
df["City"] = df["Purchase Address"].apply(lambda x: x.split(",")[1]) + "," + df["Purchase Address"].apply(lambda x: x.split(",")[2][:3])
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Hour"] = df["Order Date"].dt.hour
all_data = df[df["Order ID"].duplicated(keep=False)]
all_data["Grouped"] = df.groupby("Order ID")["Product"].transform(lambda x: ",".join(x))
product_group = df.groupby("Product")
quantity_ordered = product_group.sum()["Quantity Ordered"]


#Calculate maximum sale in the month
max_sales = df["Sales"].max()
print("Max sales: ",max_sales)      #Maximum sale in the month

#Calculate the most oftenly sold together
all_data = all_data[["Order ID","Grouped"]].drop_duplicates()
count = Counter()
for row in all_data["Grouped"]:
    row_list = row.split(",")
    count.update((Counter(combinations(row_list,2))))

print(count.most_common(10)[0])        #Most oftenly sold together

#Price of each item
price = df.groupby("Product").mean()["Price Each"]
print(price)

#Plot graph between date and sales
date_range = range(1,31)
df["Date"] = pd.to_numeric(df["Date"])
results1 = df.groupby("Date").sum()
plt.bar(date_range,results1["Sales"])
plt.xticks(date_range)
plt.title("Graph between Date and Sales")
plt.xlabel("Dates in April")
plt.ylabel("Sales in April(in $)")

plt.show()

#Plot graph between City and Sales
city_range = [city for city, all_data in df.groupby("City")]
results2 = df.groupby("City").sum()
plt.bar(city_range,results2["Sales"])
plt.xticks(city_range,rotation = "vertical",size=7)
plt.title("Graph between Cities and Sales")
plt.xlabel("Cities")
plt.ylabel("Sales in April(in $)")

plt.show()

#Plot graph between Hour and Sales
hour_range = [hour for hour, all_data in df.groupby('Hour')]
plt.plot(hour_range, df.groupby(["Hour"]).count())
plt.xticks(hour_range)
plt.title("Graph between Hour and Sales")
plt.xlabel("Time(in hour)")
plt.ylabel("Sales in April(in $)")
plt.grid()

plt.show()

#Plot graph between Product and Product Quantity
products = [product for product, all_data in product_group]
plt.bar(products,quantity_ordered)
plt.xticks(products,rotation="vertical",size=8)
plt.xlabel("Product")
plt.ylabel("Product quantity")

plt.show()