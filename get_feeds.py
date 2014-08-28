import requests
from facepy import GraphAPI
import pprint
from pymongo import MongoClient
from bson.son import SON

def p(x):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(x)

def get_name_by_id(graph, userid):
    person = graph.get('/'+ str(userid))
    print(person['name'])

token = 'secret-token'
graph = GraphAPI(token)

client = MongoClient('localhost', 27017)
db = client.likes
like_table = db.like_table

counter = 1
feeds = graph.get('userid/feed?limit=1')


while True:
    try:
        likes = feeds['data'][0]['likes']
        while True:
            try:
                for m in likes['data']:
                    like_table.insert(m)
                likes = requests.get(likes['paging']['next']).json()
            except KeyError:
                print("keyerror in likes pagination")
                break
        if(counter == 30):
            break
        counter = counter + 1
        feeds = requests.get(feeds['paging']['next']).json()
    except KeyError:
        print("keyerror happened")
        break



list = (like_table.aggregate([
    {'$group': {
        '_id': '$id',
        'count': {'$sum': 1}}
    },
    {"$sort": SON([("count", -1), ("_id", -1)])}
]))
#

for k in list['result']:
    print(k['_id'])
    print(k['count'])