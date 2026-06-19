# AI Toolbox - Portfolio

## Overview
A local AI toolbox powered entirely by offline models. All data stays on your machine - no cloud, no API costs, no privacy leaks. Built as a demo for potential clients who need private, local AI solutions.

## Features
1. **Text Summarizer** - Input any text, get a Chinese summary in 3 detail levels (brief/moderate/detailed). Powered by qwen3:8b via Ollama.
2. **RAG Knowledge Base QA** - Upload documents, ask questions, get answers with source citations. Uses ChromaDB + nomic-embed-text for semantic search.
3. **AI Image Generation** - ComfyUI + Stable Diffusion 1.5, runs on local GPU (AMD aware).
4. **Dify Platform** - Full visual AI app builder running in Docker (12 containers), Ollama integration.

## Tech Stack
| Layer | Technology |
|-------|-----------|
| LLM | Ollama + qwen3:8b (8.2B params) |
| Embedding | nomic-embed-text (768-dim) |
| Vector DB | ChromaDB |
| Backend | Python http.server |
| Frontend | Vanilla HTML/CSS/JS |
| Container | Docker + docker-compose |
| Image Gen | ComfyUI + SD 1.5 |
| IDE | Cursor (AI-assisted) |

## Architecture
```
Browser (toolbox.html)
    |
    v
Toolbox Backend (:8888)
    |-----------|-----------|
    v           v           v
Summarize   RAG Query   RAG Upload
    |           |           |
    v           v           v
Ollama API  ChromaDB    File System
(:11434)    (local)     (D:/Lobster/)
```

## Screenshots
[Screenshots placeholder - to be added]

## Key Achievements
- 7-day build from zero to full AI stack
- Chinese username path compatibility fix (OLLAMA_MODELS migration)
- Docker Hub / HuggingFace China mirror workaround
- AMD GPU compatibility handling

## Contact
[Contact info placeholder]

---
Built by: AI-assisted development (Cursor + Claude)
Date: 2026.06.15
Version: 1.0
