const API = "http://localhost:8888";

chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: "review-code",
        title: "AI Code Review - Find bugs & improvements",
        contexts: ["selection"]
    });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
    if (!info.selectionText || info.menuItemId !== "review-code") return;

    const code = info.selectionText.trim();
    if (code.length < 10) return;

    try {
        const resp = await fetch(`${API}/review`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code, language: "auto" })
        });
        const data = await resp.json();

        await chrome.storage.local.set({
            review: data.review || "No review returned",
            code_snippet: code.substring(0, 300)
        });
    } catch (e) {
        await chrome.storage.local.set({
            review: `Error: ${e.message}. Is the toolbox running?`,
            code_snippet: code.substring(0, 300)
        });
    }
});
