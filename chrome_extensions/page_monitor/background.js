// Alarm listener
chrome.alarms.onAlarm.addListener(async (alarm) => {
    if (!alarm.name.startsWith("monitor_")) return;
    const idx = parseInt(alarm.name.split("_")[1]);

    const data = await chrome.storage.local.get(["monitors"]);
    const monitors = data.monitors || [];
    if (idx >= monitors.length) return;

    const monitor = monitors[idx];

    try {
        // Fetch the page content
        const resp = await fetch(monitor.url);
        const text = await resp.text();

        // Extract readable text (strip HTML tags)
        const cleanText = text.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();

        if (monitor.lastContent) {
            // Simple similarity check
            const similarity = textSimilarity(monitor.lastContent, cleanText);
            if (similarity < 0.95) {
                monitor.hasChanged = true;
                chrome.notifications.create(`change_${idx}`, {
                    type: "basic",
                    iconUrl: "icon.png",
                    title: "Page Changed!",
                    message: `${monitor.url}\nSimilarity: ${(similarity * 100).toFixed(1)}%`
                });
            } else {
                monitor.hasChanged = false;
            }
        }

        monitor.lastContent = cleanText;
        monitor.lastCheck = new Date().toLocaleString();
        monitors[idx] = monitor;
        await chrome.storage.local.set({ monitors });

    } catch (e) {
        console.error(`Monitor ${idx} failed:`, e.message);
    }
});

// Simple text similarity (Jaccard-like on word level)
function textSimilarity(a, b) {
    const wordsA = new Set(a.toLowerCase().split(/\s+/).slice(0, 500));
    const wordsB = new Set(b.toLowerCase().split(/\s+/).slice(0, 500));
    const intersection = [...wordsA].filter(w => wordsB.has(w)).length;
    const union = new Set([...wordsA, ...wordsB]).size;
    return union === 0 ? 1 : intersection / union;
}

// Re-register alarms on startup
chrome.runtime.onStartup.addListener(async () => {
    const data = await chrome.storage.local.get(["monitors"]);
    const monitors = data.monitors || [];
    monitors.forEach((m, i) => {
        chrome.alarms.create(`monitor_${i}`, { periodInMinutes: m.interval * 60 });
    });
});
