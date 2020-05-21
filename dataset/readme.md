# 参考目录结构
```
.
├── baidu_stopwords.txt
├── bert-base-squad2
│   ├── config.json
│   ├── pytorch_model.bin
│   └── vocab.txt
├── gen-info.py
├── info.dump
├── readme.md
└── xlore.property.list.ttl
```

# xlore_qa.py 所需的文件
1. baidu_stopwords.txt # download from https://github.com/goto456/stopwords.git
2. info.dump # run gen-info.py, needs xlore.infobox.ttl
3. xlore.property.list.ttl # download from xlore

# bert_qa.py 所需的文件
bert-base-squad2 下的模型
