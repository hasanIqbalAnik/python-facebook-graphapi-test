import facebook # pip install facebook-sdk
import json
from facepy import *
import nltk
import hashlib
import unicodedata


token = "my-secret-token"
graph = facebook.GraphAPI(token)

profile =  graph.get_object('/me/friends')

for k in profile['data']:
	print k['name']

	