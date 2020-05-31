print("[auto-fill]")
dic = {}
with open('../dataset/webdict/webdict_with_freq.txt', encoding = 'utf8') as f:
    for st in f.readlines():
        word, freq = st.strip().split()
        freq = int(freq)
        if freq < 150:
            continue
        for i in range(len(word)):
            if word[:i+1] not in dic:
                dic[word[:i+1]] = []
            dic[word[:i+1]].append((word, freq))

for token in dic:
    lst_raw = dic[token]
    mp = {}
    for st, freq in lst_raw:
        mp[st] = freq
    for st, freq in lst_raw:
        for i in range(len(st) - 1):
            if st[:i+1] in mp and mp[st[:i+1]] < freq * 10:
                mp.pop(st[:i+1])
    lst_new = []
    for x in mp:
        lst_new.append((x, mp[x] * len(x)))
    lst_new.sort(key = lambda x: x[1], reverse = True)
    dic[token] = lst_new
print("[auto-fill] Init end")

def auto_fill(st):
    if st in dic:
        lst = dic[st]
        print(lst)
        lst = list(map(lambda x: x[0], lst[:min(len(lst), 5)]))
        return lst
    else:
        return []

if __name__ == '__main__':
    print(auto_fill('北京'))
    