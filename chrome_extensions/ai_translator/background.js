const API = "http://localhost:8888";

// Create right-click context menu
chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: "translate-zh-en",
        title: "AI Translate: Chinese -> English",
        contexts: ["selection"]
    });
    chrome.contextMenus.create({
        id: "translate-en-zh",
        title: "AI Translate: English -> Chinese",
        contexts: ["selection"]
    });
    chrome.contextMenus.create({
        id: "translate-ja-zh",
        title: "AI Translate: Japanese -> Chinese",
        contexts: ["selection"]
    });
});

// Handle menu clicks
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
    if (!info.selectionText) return;

    const langMap = {
        "translate-zh-en": "English",
        "translate-en-zh": "Chinese",
        "translate-ja-zh": "Chinese"
    };
    const targetLang = langMap[info.menuItemId] || "Chinese";
    const text = info.selectionText.trim();

    try {
        const resp = await fetch(`${API}/translate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, target_lang: targetLang })
        });
        const data = await resp.json();

        if (data.translation) {
            // Store result for popup display
            await chrome.storage.local.set({
                translation: data.translation,
                original: text,
                lang: targetLang
            });
        }
    } catch (e) {
        await chrome.storage.local.set({
            translation: `Error: ${e.message}`,
            original: text,
            lang: targetLang
        });
    }
});
