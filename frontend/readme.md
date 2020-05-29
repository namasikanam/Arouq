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
    "answer": QA 的答案
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