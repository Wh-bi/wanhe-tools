document.getElementById("cleanBtn").addEventListener("click", async () => {
    const btn = document.getElementById("cleanBtn");
    const loading = document.getElementById("loading");
    const result = document.getElementById("result");

    const options = {};
    if (document.getElementById("cookies").checked) options.cookies = true;
    if (document.getElementById("cache").checked) options.cache = true;
    if (document.getElementById("history").checked) options.history = true;
    if (document.getElementById("localStorage").checked) options.localStorage = true;

    const hasSelection = Object.values(options).some(v => v);
    if (!hasSelection) {
        result.textContent = "Select at least one item to clean.";
        result.className = "result error show";
        return;
    }

    btn.disabled = true;
    loading.style.display = "block";
    result.classList.remove("show");

    try {
        const dataToRemove = {};

        // Map options to browsingData API
        if (options.cookies) dataToRemove.cookies = true;
        if (options.cache) dataToRemove.cache = true;
        if (options.history) dataToRemove.history = true;

        // Track before count for reporting
        let removedCount = 0;

        // Remove browsing data (cookies/cache/history)
        if (dataToRemove.cookies || dataToRemove.cache || dataToRemove.history) {
            await chrome.browsingData.remove(
                { since: 0 },
                {
                    cookies: dataToRemove.cookies || false,
                    cache: dataToRemove.cache || false,
                    history: dataToRemove.history || false,
                    downloads: false,
                    formData: false,
                    passwords: false,
                    fileSystems: false,
                    pluginData: false,
                    serviceWorkers: dataToRemove.cache || false,
                    webSQL: false,
                    indexedDB: false
                }
            );
            removedCount++;
        }

        // Remove localStorage
        if (options.localStorage) {
            const tabs = await chrome.tabs.query({});
            for (const tab of tabs) {
                if (tab.url && tab.url.startsWith("http")) {
                    await chrome.scripting.executeScript({
                        target: { tabId: tab.id },
                        func: () => { localStorage.clear(); }
                    }).catch(() => {});
                }
            }
            removedCount++;
        }

        result.textContent = `Cleaned ${removedCount} data types successfully.`;
        result.className = "result success show";

    } catch (e) {
        result.textContent = `Error: ${e.message}`;
        result.className = "result error show";
    } finally {
        btn.disabled = false;
        loading.style.display = "none";
    }
});
