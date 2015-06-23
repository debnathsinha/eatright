import json
import os
import re
import pdb

files = [f for f in os.listdir('.') if re.match(r'wf-.*\.json', f)]
print files
for file in files:
    print file
    if file not in ['wf-82-516.json', 'wf-84-560.json', 'wf-85-529.json','wf-85-568.json','wf-85-576.json', 'wf-85-577.json']:
        with open(file) as data_file:
            data_str = data_file.readlines()[0]
            data_str = unicode(data_str, 'iso-8859-15')
            #data_str = data_str.decode('latin-5', 'replace')
            data = json.loads(data_str)
            items = data[u'data']['items']
            for item in items:
                print item['name']

#with open('wf-82-516.json') as data_file:
#    data = data_file.readlines()[0]
#    print data[183180:183190]
