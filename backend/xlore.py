import re
import csv
import jieba
import requests
import bisect
import pickle
import pymysql
import random
from utils import remove_stopwords


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

        if cnt % 10000 == 0: print("\rfinish {}".format(cnt), end = "")
    print("\n total {}".format(len(dic)))
dic.sort()
print("[xlore.property.list] Init End")

print("[xlore.infobox]")
db = pymysql.connect("localhost", "root", "123456", "xlore", charset='utf8')
cursor = db.cursor()
print("[xlore.infobox] Init End")

def xlore_get(word): # may throw exception
    resp = requests.get('http://api.xlore.org/query?word=', params = {'word': word})
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
        for uri in uris:
            print("    [URI] ", uri['label'], uri['uri'], flush = True)
            relations = get_relations(uri['uri'])
            print("    [Relation] ", relations, flush = True)
            for item in relations:
                score = 0
                for s in item[0]:
                    score += 1 if s in token_string and s not in token else 0
                if score > mx:
                    mx = score
                    QA_ret = item[1]
                    print("[Answer]", QA_ret, item)
                print("      [Item] ", item[0], item[1], score, flush = True)
            if uri['label'] == token and len(relations) > 2:
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
        print(assign)
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

if __name__ == '__main__':
    print(run("今天是个好天气"))
    print(run("原子的定义"))
    print(run("清华大学"))
