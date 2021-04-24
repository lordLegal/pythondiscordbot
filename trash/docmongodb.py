import pymongo
from pymongo import MongoClient


cluster = MongoClient("")

db = cluster["Ok-Bot"]
collection = db["casino-infos"]

#post1 = {"name":"mitik","score":129487124,"pic lvl":11248}
# collection.insert_one(post1)


collection.update_one({"_id": 0}, {"$inc": {"Uid": 0}})
#post1 = {"_id":0,"name":"Ok Coin","value":0}
# collection.insert_one(post1)
# collection.insert_many([post1,post2])
'''
bestlist = {}

cursor = collection.find({})
for document in cursor:
        Rname = document["name"]
        Rscore = document["score"]
        bestlist[Rname] = Rscore

sort_bestlist = sorted(bestlist.items(), key=lambda x: x[1], reverse=True)


for i in sort_bestlist:
    print(i[0], i[1])
'''


#results = collection.find({"score":""})
#results = collection.find({"name":"bill", "score":6})

# for result in results:                             #GOES TROUH ALL DATABASE
#    print(result["name"])


# results2 = collection.find_one({"name":"mitik"})           # ONLY ONE
#allah = collection.find_one({"name":""})
# print(allah)

#post1 = {"Uid":459814977973256202,"allah1":129487124}
# collection.insert_one(post1)
#post1 = {"_id":0,"name":"Ok Coin","value":0,"lastchange":0}
# collection.insert_one(post1)

# collection.update_one({"_id":0},{{"score":score}})

# collection.update_one({"_id":0},{"$inc":{"score":0}})
# collection.delete_one({"name":"flip"})
#results3 = collection.delete_many({"_id":0,})

# results4 = collection.update_many({"_id":5},{"$set":{"name":"tim2"}})  #YOU CAN UPDATE AND INSERT NEW THINGS
# results4 = collection.update_many({"_id":5},{"$inc":{"score":5}})       #YOU CAN ADD 5

#collection.find({"btc": {"$exists": True}})

#post_count = collection.count_documents({})
# print(post_count)
