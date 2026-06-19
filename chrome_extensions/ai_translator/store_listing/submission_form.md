# Edge Add-ons Submission - AI Translator

## Extension Name (English)
AI Translator - Local AI Translation

## Extension Name (Chinese)
AI 网页翻译器

## Short Description
Right-click to translate any selected text using local AI. Supports EN->ZH, ZH->EN, JA->ZH. Zero cost, no cloud.

## Full Description
AI Translator lets you translate selected text on any webpage with a right-click. Powered by your local Ollama models, translations happen entirely on your machine - no data ever leaves your computer.

Two ways to use:
1. Right-click menu: Select text on any page, right-click, choose target language. Translation result appears in the extension popup.
2. Extension popup: Click the extension icon to view your last translation result.

Supported languages: English -> Chinese | Chinese -> English | Japanese -> Chinese

Features:
- Zero API costs, fully local AI
- No registration required
- Data privacy guaranteed
- Lightweight and fast

Requirements: Ollama running locally with qwen3 models and AI Toolbox backend (localhost:8888).

## Search Keywords
AI, translator, translation, local, ollama, right-click, context menu, Chinese, English, 翻译

## Category
Productivity

## Privacy Statement
This extension processes translation requests entirely locally. Selected text is sent only to localhost:8888 (your AI Toolbox backend). No data is collected, stored, or transmitted to any external server.

## Permissions Justification
- contextMenus: To add right-click translation options
- activeTab: To read selected text on the current page
- storage: To cache the last translation result for popup display
- scripting: To access page content for translation
