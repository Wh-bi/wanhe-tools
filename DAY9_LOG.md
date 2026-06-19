# Day 9 日志 | 2026.06.15

## 完成项
- [x] start_toolbox.bat：一键启动工具箱（后台后端 + 3秒等待 + 提示URL）
- [x] watchdog.py：30秒间隔健康检查，连续2次失败自动重启，日志写 watchdog.log
- [x] 使用日志系统：
  - /summarize 记录：时间、输入字数、输出字数
  - /rag/query 记录：时间、问题前30字、chunk数
  - 写 D:\Lobster_Workspace\sandbox\usage.log
  - GET /stats 返回当日/累计统计 JSON
- [x] 知识库预载：
  - WEEK1_REVIEW.md（1569字→7 chunks）
  - PORTFOLIO.md（1799字→8 chunks）
  - 查询「第一阶段完成哪些项目」→ 检索到 WEEK1_REVIEW.md#0，回答列出 Cursor/Ollama/RAG/摘要器
- [x] 桌面整理：
  - 3 个快捷方式全部可用
  - 删除 10 个 sandbox 临时文件
  - 创建桌面「接单记录.md」空表格

## 技术要点
- subprocess.CREATE_NO_WINDOW 隐藏 watchdog 重启时的命令行窗口
- time.strftime + date.today 生成带日期的日志和统计
- ChromaDB 增量上传（collection.add 追加，不覆盖旧数据）
- nomic-embed-text 中文检索测试：faq.txt 距离 291 < WEEK1_REVIEW.md 距离 331

## 遇到的问题
1. http.server 单线程无法处理并发→多查询时第二个请求打崩后端
   - 解决：改为顺序单查询测试
2. 桌面 emoji 文件名（📋）写入时 Python print 报 UnicodeEncodeError
   - 影响仅终端显示，文件内容正确
   - 后续重命名为纯中文文件名
3. 后端进程 PID 变化频繁→每次操作前 netstat 查端口再 kill

## 统计接口验证
```
GET /stats → {"today":{},"total":{}}（首次启动后无数据）
```
