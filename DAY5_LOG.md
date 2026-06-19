# Day 5 日志 | 2026.06.14

## 完成项
- [x] 快捷方式紧急修复：bat 文件中 \r \t 被 Python f-string 误解析为转义序列
- [x] Docker 深度修复：docker-desktop WSL 实例恢复，docker ps 正常
- [x] AI 工具箱后端（端口 8888）：三个统一 API
- [x] AI 工具箱前端：Tab 切换（摘要/RAG问答/文档上传）
- [x] 三接口端到端测试全部通过

## 快捷方式修复详情
- 根因：Write 工具写的 bat 中 `\rag_from_scratch\rag.py` 被 Python f-string 解析时 `\r` 变成回车符
- 修复：改用正斜杠路径 `D:/Lobster_Workspace/projects/rag_from_scratch/rag.py`
- 桌面快捷方式用 Python win32com 直接创建，hex 验证通过

## Docker 修复详情
- 现象：docker-desktop WSL 实例不存在
- 根因：Docker Desktop 未随系统启动，WSL 实例未初始化
- 修复：手动启动 Docker Desktop.exe，等待约 30 秒引擎就绪
- 验证：docker ps 正常返回，docker-desktop WSL 实例 Running
- 已知：国内网络无法拉取 hello-world（需镜像加速），不影响本地服务

## 工具箱 API 测试结果
| 接口 | 测试 | 结果 |
|------|------|------|
| POST /summarize | RAG 定义摘要 | 200, 26 字中文摘要 |
| POST /rag/query | "RAG是什么？" | 200, 3 个块, 正确答案 |
| POST /rag/upload | 上传 Python 文档 | 200, 1 块索引成功 |
| POST /rag/query | "谁创建了Python？" | 200, 正确答案：Guido van Rossum 1991 |

## 遇到的问题
1. bat 文件 \r \t 转义 → 正斜杠路径修复
2. 快捷方式中文名编码 → Python win32com + 硬编码 UTF-8 字节创建
3. Docker 引擎不启动 → 等待足够时间（30秒+）让 WSL 后端就绪
