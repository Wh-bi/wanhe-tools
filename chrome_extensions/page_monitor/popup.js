// Load and display monitored pages
function renderList() {
    chrome.storage.local.get(["monitors"], (data) => {
        const monitors = data.monitors || [];
        const list = document.getElementById("list");
        if (monitors.length === 0) {
            list.innerHTML = '<div style="text-align:center;color:#64748b;padding:20px">No pages monitored yet.</div>';
            return;
        }
        list.innerHTML = monitors.map((m, i) => `
            <div class="item">
                <div class="url">${m.url}</div>
                <div class="meta">
                    <span>Every ${m.interval}h | Last: ${m.lastCheck || "Never"}</span>
                    <span class="${m.hasChanged ? 'changed' : 'same'}">${m.hasChanged ? 'CHANGED' : 'Same'}</span>
                </div>
                <button class="btn danger" style="margin-top:4px;font-size:.65rem;padding:3px 8px" data-idx="${i}">Remove</button>
            </div>
        `).join("");

        // Bind remove buttons
        list.querySelectorAll("button[data-idx]").forEach(btn => {
            btn.addEventListener("click", () => {
                const idx = parseInt(btn.dataset.idx);
                monitors.splice(idx, 1);
                chrome.storage.local.set({ monitors }, renderList);
                // Clear alarm for this index
                chrome.alarms.clear(`monitor_${idx}`);
            });
        });
    });
}

// Add new monitor
document.getElementById("addBtn").addEventListener("click", () => {
    const url = document.getElementById("url").value.trim();
    const interval = parseInt(document.getElementById("interval").value);

    if (!url || !url.startsWith("http")) {
        alert("Please enter a valid URL starting with http:// or https://");
        return;
    }

    chrome.storage.local.get(["monitors"], (data) => {
        const monitors = data.monitors || [];
        monitors.push({
            url,
            interval,
            lastCheck: null,
            lastContent: null,
            hasChanged: false
        });
        chrome.storage.local.set({ monitors }, () => {
            document.getElementById("url").value = "";
            // Create alarm (note: minimum is 1 minute in Chrome, we use periodInMinutes)
            const idx = monitors.length - 1;
            chrome.alarms.create(`monitor_${idx}`, { periodInMinutes: interval * 60 });
            renderList();
        });
    });
});

renderList();
