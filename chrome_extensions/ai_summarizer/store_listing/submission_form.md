# Edge Add-ons Submission Form

## Extension Name (English)
AI Web Summarizer - Local AI

## Extension Name (Chinese)
AI 网页摘要器

## Short Description
One-click webpage summarization using local AI (Ollama + qwen3). Fast mode returns in 6 seconds. Data never leaves your machine.

## Full Description
AI 网页摘要器是一款基于本地 AI 模型的浏览器扩展。点击按钮即可对当前网页生成中文摘要。

支持快速模式（qwen3:0.6b，约6秒）和深度模式（qwen3:8b，约45秒）。

所有数据处理均在本地完成，不上传任何内容到云端。无需注册、无需付费、无需 API Key。

适用于：新闻阅读、技术文档、学术论文、日常浏览。

## Search Keywords
AI, summary, summarizer, local, ollama, webpage, 摘要

## Category
Productivity (生产力工具)

## Privacy Statement
该扩展仅在用户主动点击时获取当前页面文本，发送到本地 Ollama API（localhost:11434）生成摘要。不收集、不存储、不上传任何用户数据。

## Permissions Justification
- activeTab：获取当前页面文本以生成摘要
- localhost 访问：调用本地 AI 模型（Ollama API）
