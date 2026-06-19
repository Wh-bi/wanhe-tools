# Day 1 日志 | 2026.06.13

## 完成项
- [x] Cursor v3.7.27 已安装（winget，此前完成）
- [x] Python 3.13.14 已安装（winget，此前完成）
- [x] organize_downloads.py 已生成并运行成功（下载文件夹已按类型分类）
- [x] 工作区 D:\Lobster_Workspace\ 已建立
- [x] RULES.md 已生效
- [x] Ollama v0.30.6 安装成功（winget）
- [x] qwen3:8b 模型下载完毕（5.2GB，已验证）

## 遇到的问题
1. Ollama 安装包下载速度较慢（GitHub 国际线路），最终 winget 成功
2. 手动静默安装失败，需 winget 才能无交互安装
3. cmd 输出在 bash 环境中被截断，后续用 PATH 变量直接调用

## 当前配置快照
- Cursor 版本：v3.7.27
- Python 版本：3.13.14
- Ollama 版本：v0.30.6
- Ollama 模型：qwen3:8b（下载中）
- 工作区路径：D:\Lobster_Workspace\
- 虚拟机：未安装（Day 2 待办）

## 当前配置快照（最终）
- Cursor 版本：v3.7.27
- Python 版本：3.13.14
- Ollama 版本：v0.30.6
- Ollama 模型：llama3.2:1b、qwen3:0.6b（备用）
- qwen3:8b 状态：已删除（首次拉取文件损坏，待重新下载）
- 工作区路径：D:\Lobster_Workspace\
- 虚拟机：未安装（Day 2 待办）

## 异常记录
- qwen3:8b 运行报错 "llama_model_loader: failed to load model"，首次下载文件可能不完整
- 已删除损坏的 8b，拉取 qwen3:0.6b 作为备用，同时用户自行拉了 llama3.2:1b
