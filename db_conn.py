import pymongo

url = 'mongodb+srv://prateekpppp4:prateek4@cluster0.lokolyb.mongodb.net'
client = pymongo.MongoClient(url)

db = client['employee_data']