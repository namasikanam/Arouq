# Arouq

Arouq是《搜索引擎技术基础》的课程项目，是一个demo级别的知识搜索引擎。

## QA

### 中文
* 流程：
    1. jieba 分词，去除停用词，获取到若干 token
    2. 使用 xlore api 找到每个 token 对应的 instance （也可以本地化）
    3. 从 infobox 里找到每个 insctance 对应的关系名和结果
    4. 找出现在去除停用词后的查询中，不包括当前instance的字数最多的关系名
* TODO：考虑同义词？ 使用 SQL？
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
    3. 保留所有名称完全匹配的instance的related instance，由于xlore中存在一些脏数据，增加一个特判为“该instance必须有较多的关系数”（完全匹配是对的吗？eg instance中没有“清华”，只有“清华大学”，因此查“清华”就没有相关推荐了）
    4. 以每个instance的related instance个数为权重，选出至多5个

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

## API

* URL: To Be Decided
* Method: GET
* Body:
```javascript
{
    "query": 查询字符串
    "page": 当前的页数，大于等于1
}
```

Successful Response
* Code: 200 OK
* Content:
```javascript
{
    "total": 检索到的文档总量
    "answer": QA 的答案，如果没有答案的话，就是一个空串
    "corrected": 更正的结果，如果不需要更正，就是一个空串
    "related": ["xxx", "yyy", ...] 相关实体，可能为空，至多5个
    "documents": [
        document1,
        ...
        // 这是某一个 document 的组成
        {
            "title": 标题
            "content": 内容序列，其中奇数项是需要高亮显示的内容
            "url": 链接
        },
        ...
        documentn, // n 不超过10，即一页显示的文档数量上限
    ]
}
```

## 计划

- [ ] 自动补全
- [x] 自动检查错误，提示可能是正确的搜索输入
- [ ] 分数据集检索（百度、中文维基、英文维基）
- [ ] 特殊符号处理（比如问号）
- [x] 相关查询

### QA

- [ ] 回答中文的问句
- [ ] 有的答案形如`[[bdi24915|2006年]]`，做正则匹配
- [ ] 回答英文的肯定句

### 前端

- [ ] 语音搜索
- [ ] 搜索的小图标
- [ ] Breadcrumb
- [ ] Dark Mode

## 开源协议

MIT