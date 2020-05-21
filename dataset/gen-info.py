import pickle
import re

info = []
with open('xlore.infobox.ttl', encoding='utf-8') as f:
    print("[xlore.infobox]")
    cnt = 0
    pattern = re.compile(r'<http://xlore\.org/instance/(.*?)> <http://xlore\.org/property/(.*?)> "(.*?)".*? \.')
    for st in f.readlines():
        cnt += 1
        match = re.search(pattern, st)
        if match is not None:
            ins, prop, ans = match.groups()
            info.append((ins, prop, ans))
        if cnt % 10000 == 0: print("\rfinish {}".format(cnt), end = "") 
    print("\n total {}".format(len(info)))
info.sort()
with open('info.dump', 'wb') as f:
    pickle.dump(info, f)