# Day 3 日志 | 2026.06.14

## 完成项
- [x] 拉取 nomic-embed-text 嵌入模型（274MB）
- [x] 安装 Python 依赖：chromadb 1.5.9 + requests 2.34.2
- [x] 创建 RAG 项目结构：rag_from_scratch/
- [x] 创建测试文档：rules.txt（290字）+ faq.txt（441字）
- [x] 编写完整 rag.py（4步：加载切分→向量化→检索→生成）
- [x] 管道输入 RAG 测试 4 题，全部通过：
  - Q1「RAG是什么？」→ 正确解释检索增强生成
  - Q2「事通有哪些硬约束？」→ 准确列出 4 条
  - Q3「向量有什么用？」→ 正确说明语义相似度等用途
  - Q4「今天北京天气？」→ 正确拒绝，不瞎编
- [x] 关闭所有自动定时任务（6个）
- [x] 创建 STATE.md 永久进度文件

## 遇到的问题

### 1. Ollama 中文路径不兼容
- 现象：nomic-embed-text 加载报错 "failed to load model from C:\Users\鹈垣\..."
- 根因：Windows 用户名含中文（鹈垣），Ollama 无法处理非 ASCII 模型路径
- 解决：设置 `OLLAMA_MODELS=C:\ollama_models`，复制模型到英文路径
- 影响范围：仅 nomic-embed-text 受影响，qwen3:8b 生成模型正常

### 2. Docker 引擎未启动
- 现象：`docker ps` 报 "failed to connect to docker API"
- 根因：WSL 已安装（Ubuntu Stopped），但 Docker Desktop 引擎未启动
- 状态：已启动 WSL，但 Docker Desktop 引擎仍未就绪
- 影响：仅 Dify 平台不可用，RAG 测试不依赖 Docker

### 3. Git Bash 中文编码穿透
- 现象：通过 `python -c "..."` 传递的中文字符被破坏
- 解决：改用 PowerShell `[System.IO.File]::WriteAllText` 或 Python base64 编码传递

### 4. PowerShell `$_` 变量被 Bash extglob 拦截
- 现象：`Where-Object { $_.Name -match ... }` 中的 `$_` 被 bash 解释
- 解决：将 PowerShell 脚本写入 .ps1 文件后执行

## 技术要点
- RAG 三步流程：索引 → 检索 → 生成
- 嵌入模型（nomic-embed-text）负责向量化，生成模型（qwen3:8b）负责回答
- ChromaDB 作为本地向量数据库存储
- Ollama 提供统一的 API 接口（生成 + 嵌入）
