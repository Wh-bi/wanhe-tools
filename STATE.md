# 事通 T0 最终态
更新：2026.06.20

## 当前状态：等待 Edge 审核 + 等待人类完成一次性操作

## 资产总览

| 类别 | 数量 | 详情 |
|------|------|------|
| Chrome 插件 | 10 | 1审核中 + 9待提交 |
| 工具箱 API | 7 | 24/7运行 |
| 落地页 | 1 | landing_page/index.html |
| Gumroad 模板 | 3 | Pro终身$19 / 单插件$3 / 5件套$9 |
| 自动化脚本 | 3 | daily_check / watchdog / edge_submitter |
| Docker 服务 | 12容器 | Dify全栈 |
| Ollama 模型 | 4 | 8b/0.6b/llama3.2/nomic-embed |

## 巡检状态（2026.06.20 00:45）
```
Ollama:   OK - 4 models online
Toolbox:  OK - 20 docs
Docker:   OK - 12 containers
Plugins:  OK - 10 plugins
```

## 人类一次性操作后 → 全自动循环启动：
```
GitHub 推送 → Pages 上线 → 搜索引擎收录 → 自然流量 → 插件安装 → 付费转化
Edge 审核通过 → 自动提交 9 个插件 → 全部上架 → 商店搜索流量 → 安装 → 付费
```

## 待人类操作
- [ ] 创建 GitHub 仓库 → 给事通 Token
- [ ] 在 Gumroad 创建 3 个产品
- [ ] （可选）安装 ngrok 暴露公网
- [ ] Edge 审核通过后确认提交

## 一次性操作指南
`D:\Lobster_Workspace\一次性操作.md`
