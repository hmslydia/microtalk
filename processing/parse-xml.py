from pprint import pprint

import operator


import xml.etree.ElementTree as ET
tree = ET.parse('../ACE2004/data/English/nwire/APW20001001.2021.0521.alf.xml')
#tree = ET.parse('../ACE2004/data/English/nwire/APW20001002.0615.0146.alf.xml')
root = tree.getroot()
doc = root[0]

#entities = doc.findall('//entity_mention')
entities = doc.findall("./composite_entity/entity")

'''
import pymongo
con = pymongo.Connection(host='127.0.0.1', port=3002)
db = con['local']
entity_collection = db.entities
'''

entityObjs = []
for entity in entities:
    entity_type = entity.attrib['TYPE']
    entity_subtype = ''
    if 'SUBTYPE' in entity.attrib:
        entity_subtype = entity.attrib['SUBTYPE']
    
    entity_mentions_for_entity = entity.findall('./entity_mention')
    for mention in entity_mentions_for_entity:
        extent_charseq = mention[0][0]
        #print extent_charseq.attrib
        text = extent_charseq.text
        start = extent_charseq.attrib['START']
        end = extent_charseq.attrib['END']

        entityObj = {
            'text':text,
            'start':int(start),
            'end':int(end),
            'type':entity_type,
            'subtype': entity_subtype,
            'docid': 0        
        }
        #c += 1
        #entity_collection.insert(entityObj)
        entityObjs.append(entityObj)
    

entityObjs.sort(key = lambda x: x['start'])

with open('entities.js', 'wt') as out:
    pprint(entityObjs, stream=out)
    
print len(entityObjs)

tree = ET.parse('../ACE2004/data/English/nwire/APW20001001.2021.0521.sgm')
#tree = ET.parse('../ACE2004/data/English/nwire/APW20001002.0615.0146.sgm')
root = tree.getroot()

allText = []
children = root.getchildren()
for child in children:
    childText = child.text
    allText.append(childText)
    if 'SOURCE' in child.attrib:
        allText.append(child.attrib['SOURCE'])
    grandchildren = child.getchildren()
    for grandchild in grandchildren:
        if grandchild.tag != 'TEXT':
            grandchildText = grandchild.text
            allText.append(grandchildText)
    
print allText
t = root.findall('./BODY/TEXT')[0].text

textParagraphs = t.split('\n\n')


def getAllTextLength():
    length = 0
    for text in allText:
        length += len(text)
    return length
    

docObj = [{
    'num' : 0,
    'paragraphs': textParagraphs,
    'allText' : allText,
    'offset' : getAllTextLength()
}]
with open('documents.js', 'wt') as out:
    pprint(docObj, stream=out)