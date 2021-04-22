import pymongo
client = pymongo.MongoClient(
    "mongodb+srv://admin:Gnsv2u00@cluster0.n69bg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mydb = client["pythondiscordbot"]
gu = mydb["guilds"]
a = gu.find_one({"_id": 815493412877893643})
print(a)
#g = a.toString()
