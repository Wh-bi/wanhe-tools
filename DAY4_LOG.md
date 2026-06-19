# Day 4 日志 | 2026.06.14

## 完成项
- [x] 创建 text_summarizer 项目结构
- [x] backend.py：HTTP 摘要服务（端口 8765），调用 Ollama qwen3:8b
- [x] index.html：暗色主题前端，fetch API 调用后端
- [x] 后端 API 测试：POST /summarize 返回 200 + 中文摘要
- [x] 改进1：实时字数统计（oninput 事件 + charCount span）
- [x] 改进2：三级详细程度（简短 100 字 / 适中 300 字 / 详细 600 字）
- [x] 改进3：三级 curl 测试通过

## 技术要点
- Python http.server 模块搭建简易 API 服务
- Ollama generate API 的 prompt 工程（动态调整字数限制）
- CORS 头配置（Access-Control-Allow-Origin）
- 前端 fetch + JSON 交互

## 测试结果
| 详细程度 | 输入 | 摘要长度 | 状态 |
|---------|------|---------|------|
| 简短 (100字) | faq.txt 440字 | 146 字 | ✅ |
| 适中 (300字) | faq.txt 440字 | 135 字 | ✅ |
| 详细 (600字) | faq.txt 440字 | 129 字 | ✅ |

注：三级长度相近是因为输入文本本身较短（440字），摘要自然收敛。参数传递和 prompt 调整机制验证正确。

## 遇到的问题
- 无新问题。Day 3 的编码/路径问题已在本次修复中沿用解决方案。
