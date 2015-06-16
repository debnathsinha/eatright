import json

with open('wf-90-573.json') as data_file:
    data = json.loads(data_file.readlines()[0])
    items = data[u'data']['items']
    for item in items:
        print item['name']
