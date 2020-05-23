print("[stopwords]")
stopwords = set()
with open('../dataset/baidu_stopwords.txt', encoding='utf-8') as f:
    for st in f.readlines():
        stopwords.add(st.strip())
    print("total: {}".format(len(stopwords)))
print("[stopwords] Init End")

def remove_stopwords(wordlist):
    return list(filter(lambda x: x not in stopwords, wordlist))
