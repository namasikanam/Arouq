import re
import csv
import jieba
import requests
import bisect
import pickle
import pymysql
import random
import synonyms
import json
from utils import remove_stopwords
from utils import contain_english

dic = []
print("[xlore.property.list]")
with open('../dataset/xlore.property.list.ttl', encoding='utf-8') as f:
    cnt = 0
    label = re.compile(r'<(.*?)> rdfs:label "(.*?)"@(.*?) \.')
    fullname = re.compile(r'<(.*?)> property:fullname "(.*?)"@.*? \.')
    for st in f.readlines():
        cnt += 1
        match = re.search(label, st)
        if match is not None:
            id, name, language = match.groups()
            dic.append((id, name))
        if cnt % 10000 == 0:
            print("\rfinish {}".format(cnt), end = "")
    print("\n total {}".format(len(dic)))
dic.sort()
print("[xlore.property.list] Init End")

print("[xlore.infobox]")
db = pymysql.connect("localhost", "root", "123456", "xlore", charset='utf8')
cursor = db.cursor()
print("[xlore.infobox] Init End")

def xlore_get(word): # may throw exception
    resp = requests.get('http://api.xlore.org/query', params = {'word': word})
    return resp.json()

def xlore_instances(word):
    try:
        resp = xlore_get(word)
    except Exception as err:
        print("Error at {}: {}".format(word, err))
        return []
    ret = []
    for ins in resp['Instances']:
        related = []
        for item in ins['Related Instances']:
            related.append(item['Label'])
        ret.append({
            'label': ins['Label'],
            'uri': ins['Uri'].split('/')[-1],
            'related': related})
    return ret

def get_tokens(question):
    seg_list = jieba.lcut(question)
    return remove_stopwords(seg_list)

def info_search(uri):
    cmd = "select * from info where instance = '{}'".format(uri)
    cursor.execute(cmd)
    ret = cursor.fetchall()
    return ret

def dict_to_name(x):
    global dic
    left = bisect.bisect_left(dic, (x, ""))
    if (dic[left][0] == x):
        return dic[left][1]
    else:
        return None

def get_relations(uri):
    ret = []
    relations = info_search(uri)
    for x in relations:
        name = dict_to_name(x[1])
        if name is not None:
            ret.append((name, x[2]))
    return ret

def run(question):
    print("[Question] ", question, flush = True)
    tokens = get_tokens(question)
    token_string = ''.join(tokens)
    mx = 0
    QA_ret = None
    related = []
    for token in set(tokens):
        print(" [Token] ", token, flush = True)
        uris = xlore_instances(token)
        syns = set()
        syns.add(token)
        syn_raw, scores = synonyms.nearby(token)
        for syn, score in zip(syn_raw, scores):
            print(syn, score)
            if score > 0.75:
                syns.add(syn)
        print("    [Synonym]", syns)
        for uri in uris:
            print("    [URI] ", uri['label'], uri['uri'], flush = True)
            relations = get_relations(uri['uri'])
            print("    [Relation] ", relations, flush = True)
            for item in relations:
                score = 0
                for s in item[0]:
                    score += 1 if s in token_string and s not in token else 0
                if uri['label'] in syns:
                    score *= 1.5
                if score > mx:
                    mx = score
                    QA_ret = item[1]
                    QA_ret = re.sub(r'\[\[.*?\|', "", QA_ret)
                    QA_ret = re.sub(r'\]\]', "", QA_ret)
                    print("[Answer]", QA_ret, item)
                print("      [Item] ", item[0], item[1], score, flush = True)
            if uri['label'] in syns and len(relations) > 2:
                related.append(uri['related'])
                print("      [Related]", uri['related'])
    related_ret = []
    max_related = 5
    if sum([len(x) for x in related]) > max_related:
        assign = [len(x) for x in related]
        total = sum(assign)
        assign = [x * max_related // total for x in assign]
        remain = total - sum(assign)
        while sum(assign) < max_related:
            x = random.randint(0, len(related) - 1)
            if assign[x] < len(related[x]):
                assign[x] += 1
        for r, a in zip(related, assign):
            related_ret.extend(random.sample(r, a))
    else:
        for x in related:
            related_ret.extend(x)
    print("[Final Score]", mx)
    print("[Related]", related_ret)
    return {
        'QA_ret': QA_ret,
        'related': related_ret,
    }

def solr(query, page):
    # Split the query by the language
    if contain_english(query):
        tokens = query.split()
        # tokens = [query]
        language = 'en'
    else:
        tokens = get_tokens(query)
        language = 'cn'
    
    # Construct the request to Solr
    query_string = ''
    for token in tokens:
        query_string += 'name:"' + token + '"^5'
        query_string += ' properties:' + token + '^0.2'
        query_string += ' article:' + token + '^1'
        query_string += ' classes:' + token + '^0.1'
    response = requests.get(f'http://localhost:8983/solr/xlore_{language}/select', params = {
        'q': query_string,

        'start': (page - 1) * 10,
        'hl': 'on',
        'hl.method': 'unified',
        'hl.snippets': 100, # A number that is larger than how many properties and classes are intended to show
        'hl.fragsize': 0,
        'hl.fl': 'name properties article', # highlight article is too complicated
        'hl.tag.pre': '<span class="highlight">',
        'hl.tag.post': '</span>'
    })
    
    res = response.json()

    ans = res['response']['docs']

    id_to_doc = {}
    for doc in ans:
        id_to_doc[doc['id']] = doc
        del doc['id']
        del doc['_version_']

    for id, highlighted in res['highlighting'].items():
        doc = id_to_doc[id]

        assert len(highlighted['name']) <= 1
        if len(highlighted['name']) == 1:
            doc['name'] = highlighted['name'][0]
        
        for prop in highlighted['properties']:
            sep_place = prop.find('::')
            p = re.sub(r'<span class="highlight">(.*)</span>', lambda matchObj: matchObj.group(1), prop[:sep_place]) + prop[sep_place:]
            j = 0
            for i in range(len(doc['properties'])):
                prop_0 = doc['properties'][i]
                prop_name = prop_0[:prop_0.find('::')]
                if prop_name in p:
                    doc['properties'][i] = p
                    doc['properties'][i], doc['properties'][j] = doc['properties'][j], doc['properties'][i]
                    j = j + 1
                    break
            
            # We only take the first several properties,
            # this number should be changed according to the effect.
            doc['properties'] = doc['properties'][:10]
        
        if len(highlighted['article']) == 1:
            # We only take the first several characters,
            # this number should be changed according to the effect.
            doc['article'] = highlighted['article'][0][:(500 if language == 'en' else 1000)]
        
        if 'classes' not in doc:
            doc['classes'] = []
        doc['classes'] = doc['classes'][:10]
    
    # for debug, please comment the following dump
    # in the production environment for performance
    if __name__ == '__main__':
        with open('response.json', 'w') as f:
            json.dump(res, f, indent = 2)

    return (res['response']['numFound'], ans)

if __name__ == '__main__':
    # print(run("今天是个好天气"))
    # print(run("原子的定义"))
    print(run("中国的人口"))
    # solr('russian minister')
    # solr('清华大学', 1)
    # solr('Tsinghua University', 1)