# Arouq

Arouq是《搜索引擎技术基础》的课程项目，是一个demo级别的知识搜索引擎。

## QA

### 中文
* 流程：
    1. jieba 分词，去除停用词，获取到若干 token
    2. 使用 xlore api 找到每个 token 对应的 instance （也可以本地化）
    3. 从 infobox 里找到每个 insctance 对应的关系名和结果
    4. 找出现在去除停用词后的查询中，不包括当前instance的字数最多的关系名
    5. 某些答案格式奇怪，需调整为用户可以接受的格式
* TODO：考虑同义词？ 
* 好的查询：原子的定义

### 英文
* 流程
    1. 分词，去停用词
    2. 在 Wikipedia 里查词
    3. 将开头喂给 bert
    4. 将其他词出现较多的位置喂给 bert
    5. 取 bert 评分最大的位置

## 相关推荐（中文）
* 流程：
    1. jieba 分词，去除停用词，获取到若干 token
    2. 使用 xlore api 找到每个 token 对应的 instance （也可以本地化）
    3. 筛选出是 token 的近义词的 instance
    4. 为避免xlore中的脏数据影响推荐，增加一个特判为“该instance必须有较多的关系数”
    5. 以每个instance的related instance个数为权重，选出至多5个

## 纠错
* 直接调库，不认为英文大小写出错是错误

## 自动补全（中文）
* 流程：
    1. 从词频表里筛选出词频大于150的词
    2. 如果词 A 是词 B 的子串，且词 A 的出现次数小于词 B 的 10 倍，那么将词 A 去掉
    3. 以词频\*长度作为一个词的评分
    4. 查询时，选出以查询词为前缀的评分最高的5个词

## 前端

安装
```bash
cd frontend/
npm install
```

运行
```bash
cd frontend/
npm start
```

## Solr 配置

1. 从[这里](https://lucene.apache.org/solr/downloads.html)下载一份 Solr 的 Binary Release 版。
2. 启动 Solr Cloud
3. 创建 xlore 的 collection （中/英文各一个）
4. 为 collection 分别配置 Schema（使用`dataset/create_schema.sh`）
5. 为中英文数据创建索引

TODO：具体的指令以后有时间再补吧。

## API
### 搜索
* Port: 8001
* URL: localhost
* Method: GET
* Body:
```javascript
{
    "query": 查询字符串
    "page": 查询的页数，大于等于1
}
```

Successful Response
* Code: 200 OK
* Content:
```javascript
{
    "total": 检索到的文档总量
    "answer": QA 的答案，如果没有答案的话，就是一个空串
    "related": ["xxx", "yyy", ...] 相关实体，可能为空，至多5个
    "documents": [
        document1,
        ...
        // 这是某一个 document 的组成
        {
            "name": 标题
            "article": 文章主题，其中需要高亮的部分已被打上 `<span class="highlight">...</span>` 的 tag
            "url": 链接
            "classes"：所属类别的列表，可能为空
            "properties"：性质列表，可能为空
        },
        ...
        documentn, // n 不超过10，即一页显示的文档数量上限
    ]
}
```

### 纠错
* Port: 8002
* URL: /correct
* Method: GET
* Body:
```javascript
{
    "query": 查询字符串
}
```

Successful Response
* Code: 200 OK
* Content:
```javascript
{
    "corrected": 更正的结果，如果不需要更正，就是一个空串
}
```

### 自动补全
* Port: 8001
* URL: /fill
* Method: GET
* Body:
```javascript
{
    "query": 查询字符串
}
```

Successful Response
* Code: 200 OK
* Content:
```javascript
{
    "result": ["xxx", "yyy", ...] 补全结果，至多5个，可能为空列表
}
```



## 计划

- [x] 自动补全（中文）
- [ ] 自动补全（英文）
- [x] 自动检查错误，提示可能是正确的搜索输入（中文）
- [x] 纠错（英文）
- [ ] 分数据集检索（百度、中文维基、英文维基）
- [ ] 特殊符号处理（比如问号）
- [x] 相关查询（中文）
- [ ] 相关查询（英文）

### QA

- [ ] 回答中文的问句
- [ ] 回答英文的肯定句

### 前端

- [ ] 语音搜索
- [ ] 搜索的小图标
- [ ] Breadcrumb
- [ ] Dark Mode

## 开源协议

MIT