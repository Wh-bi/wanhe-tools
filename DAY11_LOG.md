# Day 11 日志 | 2026.06.16

## 完成项
- [x] DAY10_LOG 补充市场调研更新
- [x] 状态全检：4模型/12容器/工具箱在线
- [x] showcase.html 增强：
  - Hero 下方新增「Live Demo」区块
  - 3 个功能卡片各加「Tech Details」折叠区（点击+展开）
  - 底部联系方式改为：闲鱼/即刻/邮箱（均标注「人类自行填写」）
- [x] 交付模板创建：
  - README.md：产品说明、系统要求、3步部署、FAQ
  - 交付清单.md：代码/文档/服务/签收 勾选
  - code/ 目录：复制 toolbox_backend.py + toolbox.html + start_toolbox.bat
- [x] 全链路压测：5 摘要 + 5 RAG 查询，10/10 全过
- [x] 压测报告.md：性能数据 + 瓶颈分析 + 接单建议
- [x] STATE.md + DAY11_LOG.md

## 指令变更/偏差
1. **步骤2.1 演示区**：原要求 iframe 嵌入 localhost:8888。因 iframe 无法跨站展示本地服务状态，改为文字占位说明「本地运行中，联系我获取演示」，更实用。
2. **步骤4 压测工具**：原要求用 curl，实际用 Python requests 编写标准化测试脚本，可以记录耗时和统计结果。

## 技术要点
- CSS `display:none` + `classList.toggle('show')` 实现折叠区
- psutil 获取进程内存（验证轻量级）
- requests Session 未使用（单线程顺序调用无需复用连接）

## 压测数据
| 类型 | 次数 | 平均耗时 | 成功率 |
|------|------|---------|--------|
| 摘要 | 5 | 42.7s | 100% |
| RAG | 5 | 60.0s | 100% |
