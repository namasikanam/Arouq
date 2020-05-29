import re
import csv
import jieba
import requests
import bisect
import pickle
import pymysql
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
        ret.append((ins['Label'], ins['Uri'].split('/')[-1]))
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

def xlore_QA(question):
    print("[Question] ", question, flush = True)
    tokens = get_tokens(question)
    token_string = ''.join(tokens)
    mx = 0
    QA_ret = None
    for token in set(tokens):
        print(" [Token] ", token, flush = True)
        uris = xlore_instances(token)
        for uri in uris:
            print("    [URI] ", uri, flush = True)
            relations = get_relations(uri[1])
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
    print("[Final Score]", mx)
    return QA_ret

if __name__ == '__main__':
    print(xlore_QA("今天是个好天气"))
    print(xlore_QA("原子的定义"))
