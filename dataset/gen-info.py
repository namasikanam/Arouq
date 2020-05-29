import pickle
import re
import pymysql

# CREATE TABLE `xlore`.`info` (
#   `instance` VARCHAR(20) NOT NULL,
#   `relation` VARCHAR(20) NOT NULL,
#   `answer` VARCHAR(500) NOT NULL);

db = pymysql.connect("localhost", "root", "123456", "xlore", charset='utf8')
cursor = db.cursor()


with open('xlore.infobox.ttl', encoding='utf-8') as f:
    print("[xlore.infobox]")
    cnt = 0
    pattern = re.compile(r'<http://xlore\.org/instance/(.*?)> <http://xlore\.org/property/(.*?)> "(.*?)".*? \.')
    for st in f.readlines():
        cnt += 1
        match = re.search(pattern, st)
        if match is not None:
            ins, prop, ans = match.groups()
            cmd = """insert into info values("{}", "{}", "{}")""".format(ins, prop, ans)
            try:
                cursor.execute(cmd)
            except Exception as e:
                print(cmd)
                print(e)
        if cnt % 10000 == 0:
            db.commit()
            print("\rfinish {}".format(cnt), end = "") 

db.commit()
cursor.execute('create index ins on info(instance);')
db.commit()
db.close()
