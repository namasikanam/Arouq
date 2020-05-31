# 参考目录结构
```
.
├── baidu_stopwords.txt
├── bert-base-squad2
│   ├── config.json
│   ├── pytorch_model.bin
│   └── vocab.txt
├── gen-info.py
├── readme.md
├── webdict
│   └── webdict_with_freq.txt
└── xlore.property.list.ttl
```

# xlore_qa.py 所需的文件
1. baidu_stopwords.txt # download from https://github.com/goto456/stopwords.git
2. A sql database generated from xlore.infobox.ttl, refer to gen-info.py
3. xlore.property.list.ttl # download from xlore

# bert_qa.py 所需的文件
bert-base-squad2 下的模型

# 自动补全所需的文件
webdict 仓库，克隆自 https://github.com/ling0322/webdict.git