# Arouq
Course Project of Fundamentals of Search Engine Technology

## QA
### 中文
* list + 二分以减少内存，现在需要8G
* 流程：
    1. jieba 分词，去除停用词，获取到若干 token
    2. 使用 xlore api 找到每个 token 对应的 instance （也可以本地化）
    3. 从 infobox 里找到每个 insctance 对应的关系名和结果
    4. 找出现在查询的字数最多的关系名
* TODO：考虑同义词？ 使用 SQL？
* 好的查询：原子的定义
