from re import A
import pymongo
client = pymongo.MongoClient(
    "mongodb+srv://admin:Gnsv2u00@cluster0.n69bg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mydb = client["pythondiscordbot"]
us_gu = mydb["user_guild"]

a = us_gu.find_one({"gu_id": "815493412877893643",
                    "ids": {"id": "282616377653592064"}})
print(a)
c = a["ids"][0]["id"]
y = int(a["ids"][3]["date"])
print(y)
print(c)
g = c
print(g)
