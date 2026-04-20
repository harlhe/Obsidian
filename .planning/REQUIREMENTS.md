# Requirements: Obsidian 学习笔记重构

**Defined:** 2026-04-20
**Core Value:** 同一主题的信息必须可在一个入口下被快速找到、快速复习、快速追溯来源

## v1 Requirements

### Information Architecture
- [ ] **IA-01**: 每个顶层目录（00-06）至少有 1 份结构化总览笔记
- [ ] **IA-02**: 总览笔记包含主题定位、核心概念、子主题索引、融合记录、延伸阅读、参考资料
- [ ] **IA-03**: 重分类后旧路径保留可跳转重定向说明

### Reclassification & Dedup
- [ ] **RECL-01**: 主题不匹配文档迁移到语义更匹配目录
- [ ] **RECL-02**: 重复/空壳文档合并到主文档并保留映射
- [ ] **RECL-03**: 输出可审计的融合记录表（source -> canonical）

### Sparse Enrichment
- [ ] **ENR-01**: 所有非空且字符数 <= 800 的目标笔记完成补强
- [ ] **ENR-02**: 补强笔记统一包含概念、机制/流程、学习要点、高频面试问答、易错点、参考资料
- [ ] **ENR-03**: 每篇补强笔记包含 2-4 条外部来源链接

### Validation
- [ ] **VAL-01**: 随机抽样检查目录一致性（至少每个顶层目录 3 篇）
- [ ] **VAL-02**: 校验总览与重定向链接可解析
- [ ] **VAL-03**: 空白文件保持不填充内容

## v2 Requirements

### Governance
- **GOV-01**: 增加自动化脚本，周期检测“新产生的稀疏笔记”
- **GOV-02**: 增加定期面经复盘模板

## Out of Scope

| Feature | Reason |
|---------|--------|
| 自动删除空白笔记 | 本轮策略要求先保留占位文件 |
| 顶层目录大改名 | 会破坏已有路径习惯与外链 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| IA-01 | Phase 1 | Complete |
| IA-02 | Phase 1 | Complete |
| IA-03 | Phase 1 | Complete |
| RECL-01 | Phase 1 | Complete |
| RECL-02 | Phase 1 | Complete |
| RECL-03 | Phase 1 | Complete |
| ENR-01 | Phase 2 | Complete |
| ENR-02 | Phase 2 | Complete |
| ENR-03 | Phase 2 | Complete |
| VAL-01 | Phase 3 | Complete |
| VAL-02 | Phase 3 | Complete |
| VAL-03 | Phase 3 | Complete |

**Coverage:**
- v1 requirements: 12 total
- Mapped to phases: 12
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-20*
*Last updated: 2026-04-20 after initial definition*
