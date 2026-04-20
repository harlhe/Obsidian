# ES 分布式搜索引擎速记（学习+面试）

## 概念
Elasticsearch（ES）是基于 Lucene 的分布式搜索与分析引擎，核心能力是全文检索、聚合分析、近实时查询。它通过分片（shard）和副本（replica）实现横向扩展和高可用。

## 机制/流程
1. 写入：文档进入主分片，刷新后可被搜索。
2. 查询：协调节点把查询广播到相关分片并聚合返回。
3. 高可用：主分片故障时，副本可提升为主分片。

## 学习要点
- 倒排索引是 ES 检索性能的核心。
- 分片数影响并发与运维复杂度，创建索引后主分片不可直接修改。
- 近实时不等于实时，refresh 间隔影响可见性与写入吞吐。

## 高频面试问答
- Q：ES 为什么快？
  A：倒排索引 + 分片并行查询 + 缓存机制（query cache / request cache）。
- Q：如何避免深分页问题？
  A：优先 `search_after` 或 scroll，而不是大 offset 的 from/size。

## 易错点
- 把 ES 当强一致事务库使用。
- 不做 mapping 设计导致字段类型冲突。

## 参考资料
- [Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Lucene Scoring](https://lucene.apache.org/core/)
- [Search After 文档](https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html)

## 实战演练清单
- 用一个真实任务做 30 分钟限时复盘：先写目标、再写步骤、最后写结果与改进点。
- 把当前主题抽成 3 个“可复述模板”：定义模板、排障模板、面试回答模板。
- 记录一次失败样例：失败现象、根因、修复策略、可复用经验。

## 复习节奏建议
- D1：通读全文，口述核心概念（3-5 分钟）。
- D3：只看“高频问答”和“易错点”，做一次自测。
- D7：结合实际项目或面试题，写一页应用案例。
- D14：回看旧结论，删除过时信息并补充新实践。

## 自测题（可直接口述）
1. 这个主题最关键的工程权衡是什么？
2. 如果要落地到你的项目，第一步应该做什么？
3. 如何定义这个主题“做成了”的验收标准？

