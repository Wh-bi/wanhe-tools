# 第一阶段复盘（2026.06.01 - 2026.06.14）

## 六大产出
| # | 项目 | 路径 | 说明 |
|---|------|------|------|
| 1 | Cursor 开发环境 | 已安装 | AI 辅助编程 IDE |
| 2 | Ollama 本地模型 | qwen3:8b / 0.6b / llama3.2:1b / nomic-embed-text | 本地大模型运行 |
| 3 | RAG 知识库引擎 | projects/rag_from_scratch/ | 从零实现的检索增强生成 |
| 4 | 文本摘要器 | projects/text_summarizer/ | Web 前后端，三级详细度 |
| 5 | AI 工具箱 | projects/ai_toolbox/ | 统一界面（摘要+RAG+上传） |
| 6 | Dify 平台 | Docker 12 容器 + localhost | 可视化 AI 应用搭建 |
| 7 | ComfyUI | projects/ComfyUI/ + SD 1.5 | AI 绘画引擎（CPU模式验证通过） |

## 五项技能
1. **AI 编程**：Cursor Ctrl+K/L/I + Tab补全工作流
2. **本地部署**：Ollama 模型管理，API 调用，中文路径修复
3. **RAG 原理**：索引→检索→生成三步，ChromaDB + 嵌入模型
4. **Web 后端**：Python http.server，CORS，前端 fetch API
5. **Docker**：容器管理，WSL 集成，国内镜像代理

## 关键踩坑
1. **中文用户名路径**：Ollama 无法加载 nomic-embed-text → 迁移 OLLAMA_MODELS 至 C:\ollama_models
2. **编码穿透**：Git Bash → PowerShell → Python 三层管道中文全部丢失 → base64 / hex 硬编码字节
3. **WSL 依赖**：Docker Desktop 引擎不启动 → 需先装 WSL2，手动启动 Docker Desktop 等30秒+
4. **Ollama 进程卡死**：CLI 触发 serve 后超时 → 先 kill 所有进程再 serve，等 GPU 检测完成
5. **bat 文件 \r \t 转义**：Write 工具写的路径被 Python f-string 误解析 → 改用正斜杠路径
6. **Docker Hub 被墙**：所有镜像拉取失败 → daocloud 代理手动拉取 + tag
7. **HuggingFace 被墙**：SD 1.5 模型下载超时 → hf-mirror.com 镜像
8. **AMD GPU 兼容**：ComfyUI 默认 Nvidia → 需 --cpu 或 DirectML

## 工具矩阵
| 功能 | 命令行 | Web 界面 | 桌面快捷方式 |
|------|--------|---------|-------------|
| 文本摘要 | - | :8765 | AI摘要器 |
| RAG 问答 | rag.py | :8888 | AI知识库 |
| 工具箱 | - | :8888 | AI工具箱 |
| Dify | - | :80 | - |
| ComfyUI | main.py | :8188 | - |

## 下一步
第二阶段：接单变现准备
- AI 绘图实战（ComfyUI + 提示词工程）
- 本地 API 服务稳定化
- 接单模板和定价策略
