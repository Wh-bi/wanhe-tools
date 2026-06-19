# Edge Add-ons Submission - AI Code Reviewer

## Extension Name
AI Code Reviewer - Local AI Code Review

## Short Description
Right-click any code snippet for instant AI review. Find bugs, security issues, and optimizations using local AI.

## Full Description
AI Code Reviewer lets you get instant code reviews by selecting code on any webpage (GitHub, Gitee, GitLab, etc.) and right-clicking. Powered by your local AI models, reviews happen entirely on your machine.

The review covers:
1. Potential bugs and logic errors
2. Performance optimization suggestions
3. Security vulnerability detection
4. Code style improvements

No cloud, no API costs, no data leaves your computer. Perfect for solo developers, code reviewers, and anyone who wants a second pair of AI eyes on their code.

Requirements: Ollama + AI Toolbox backend (localhost:8888)

## Search Keywords
code, review, AI, bug, security, optimization, developer, programming, GitHub

## Category
Developer Tools

## Privacy Statement
Selected code is sent only to localhost:8888. No data is collected, stored, or transmitted externally.

## Permissions Justification
- contextMenus: Right-click code review option
- activeTab/scripting: Read selected code
- storage: Cache review results
