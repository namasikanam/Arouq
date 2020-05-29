# Arouq

Arouq是《搜索引擎技术基础》的课程项目，是一个demo级别的知识搜索引擎。

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

### 英文
* 流程 （TODO）
    1. 分词，去停用词
    2. 在 Wikipedia 里查词
    3. 将开头喂给 bert
    4. 将其他词出现较多的位置喂给 bert
    5. 取 bert 评分最大的位置


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

## 计划

- [ ] 自动补全
- [ ] 自动检查错误，提示可能是正确的搜索输入
- [ ] 分数据集检索（百度、中文维基、英文维基）
- [ ] 特殊符号处理（比如问号）

### 前端

- [ ] 语音搜索
- [ ] 搜索的小图标
- [ ] Breadcrumb
- [ ] Dark Mode

## 开源协议

MIT