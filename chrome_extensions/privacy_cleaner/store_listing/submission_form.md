# Edge Add-ons Submission Form - Privacy Cleaner

## Extension Name (English)
Privacy Cleaner - One Click Browsing Data Cleaner

## Extension Name (Chinese)
隐私清理器

## Short Description
One-click clear cookies, cache, browsing history, and localStorage. Lightweight, no tracking, no ads.

## Full Description
Privacy Cleaner is a lightweight browser extension that lets you clean your browsing data with a single click. Select which data types to clear (cookies, cache, browsing history, localStorage) and hit the button. No configuration needed, no data collected, no ads. Perfect for privacy-conscious users who want quick cleanup without digging through browser settings.

## Search Keywords
privacy, cleaner, cookies, cache, history, browsing data, localStorage, 隐私, 清理

## Category
Productivity / Privacy & Security

## Privacy Statement
This extension does NOT collect, store, or transmit any user data. It only triggers the browser's built-in browsingData.remove() API when the user clicks the button. No external servers, no analytics, no tracking.

## Permissions Justification
- browsingData: Required to clear cookies, cache, and browsing history
- cookies: Required to clear cookie data
- storage: Required for future settings persistence
- activeTab/host_permissions: Required to clear localStorage across tabs
