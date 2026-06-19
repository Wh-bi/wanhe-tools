# Extension Packing Guide

## Pack the Extension
1. Open Chrome: chrome://extensions/
2. Enable "Developer mode" (top right)
3. Click "Pack extension"
4. Extension root directory: D:\Lobster_Workspace\chrome_extensions\ai_summarizer\
5. Leave private key blank (Chrome will generate .pem on first pack)
6. Click "Pack Extension"

## After Packing
- .crx file will be created in chrome_extensions/
- .pem file will be created in ai_summarizer/ (or parent dir)
- **MOVE .pem to** D:\Lobster_Workspace\chrome_extensions\keys\
- **NEVER lose the .pem file** - it's your identity. Without it, you can't update the extension.

## Before Uploading to Chrome Web Store
- Verify .crx installs correctly (drag to chrome://extensions/)
- Screenshots taken and added to store_listing/
- description.md content copied to store form
- $5 registration fee paid at Chrome Web Store Developer Console
