# Day 13 日志 | 2026.06.16

## 完成项
- [x] 状态全检
- [x] 工具箱模型切换功能：
  - 前端：header 右侧模型选择器（Fast 0.6b / Deep 8b）
  - 后端：/summarize + /rag/query 接受 model 参数，默认 qwen3:0.6b
  - /health 新增 default_model 字段
  - 实测验证：0.6b=6.4s, 8b=46.9s
- [x] 实时耗时显示：摘要和问答结果下方显示 Latency + Model
- [x] 优化建议书.md：基础版vs加速版+ROI计算（3年成本仅为云服务1/10）+客户话术
- [x] 接单话术追加 Q6：速度问题应答（两种模式免费+本地+不限次）
- [x] 文档分类：对外材料 vs 内部资料
- [x] STATE.md + DAY13_LOG.md

## 指令变更/偏差
1. **默认模型变更**：从 qwen3:8b 改为 qwen3:0.6b。原本8b默认导致每次45秒，客户体验差。改为0.6b默认后6秒响应，深度模式可选。
2. **接单话术追加**：在步骤外追加Q6（速度问题），因模型切换后此问题变得高频。
3. **ROI计算增补**：优化建议书额外增加了3年成本对比表（本地vs云服务vs企业外包），让客户直观看到成本优势。

## 技术要点
- 前端 select.onchange 无需额外JS，fetch时直接读 value
- 后端 model = body.get("model", MODEL) 一行实现默认值
- innerHTML 替代 textContent 以支持耗时小字的HTML标签
