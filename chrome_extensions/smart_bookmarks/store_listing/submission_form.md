# Edge Add-ons Submission - Smart Bookmarks

## Extension Name
Smart Bookmarks - AI Bookmark Manager

## Short Description
AI-powered bookmark organizer with auto-classification, deduplication, dead link detection, and instant search.

## Full Description
Smart Bookmarks is a comprehensive bookmark management tool powered by local AI (Ollama + qwen3). It helps you organize hundreds of bookmarks effortlessly.

Features:
1. AI Classification - Automatically categorize bookmarks into Work, Study, Entertainment, Tools, Social, and more with one click
2. Deduplication - Find and remove duplicate bookmarks instantly
3. Dead Link Detection - Scan all bookmarks and mark broken links in red
4. Instant Search - Filter bookmarks by keyword in real-time
5. Collapsible Categories - Browse bookmarks grouped by category
6. Statistics - Overview of total bookmarks, categories, and dead links

All processing is local - your bookmarks never leave your browser.

## Search Keywords
bookmark, manager, organize, classify, deduplicate, dead link, AI, smart, 书签, 管理

## Category
Productivity

## Privacy Statement
Bookmark data is processed entirely through Chrome APIs. AI classification requests are sent to localhost:8888. No bookmark data is uploaded to any external server.

## Permissions Justification
- bookmarks: Required to read, organize, and remove bookmarks
- storage: Required for caching classification results
