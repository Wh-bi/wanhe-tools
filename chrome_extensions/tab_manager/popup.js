let allTabs = [];
let searchQuery = "";
let showSessions = false;

// Load tabs on open
async function loadTabs() {
    allTabs = await chrome.tabs.query({});
    const windows = await chrome.windows.getAll();
    // Attach window index
    allTabs.forEach(t => {
        t.windowIdx = windows.findIndex(w => w.id === t.windowId) + 1;
    });
    renderStats();
    renderTabs();
}

function renderStats() {
    const windows = new Set(allTabs.map(t => t.windowId)).size;
    const discarded = allTabs.filter(t => t.discarded).length;
    const memMB = allTabs.length * 80; // rough estimate
    document.getElementById("stats").innerHTML =
        `Tabs: <span>${allTabs.length}</span> | Windows: <span>${windows}</span> | Sleeping: <span>${discarded}</span> | ~<span>${memMB}MB</span>`;
}

async function renderTabs() {
    const q = searchQuery.toLowerCase();
    let filtered = allTabs;
    if (q) {
        filtered = allTabs.filter(t =>
            (t.title || "").toLowerCase().includes(q) || (t.url || "").toLowerCase().includes(q)
        );
    }

    if (showSessions) {
        renderSessions();
        return;
    }

    // Group by window
    const groups = {};
    filtered.forEach(t => {
        const key = `Window ${t.windowIdx}`;
        if (!groups[key]) groups[key] = [];
        groups[key].push(t);
    });

    let html = "";
    for (const [win, tabs] of Object.entries(groups)) {
        html += `<div class="window-group"><div class="win-header">${win} (${tabs.length} tabs)</div>`;
        tabs.forEach(t => {
            html += `<div class="tab-item" onclick="chrome.tabs.update(${t.id},{active:true});chrome.windows.update(${t.windowId},{focused:true})">
                <span class="title ${t.discarded ? 'discarded' : ''}">${t.title || t.url}</span>
                <span class="close-btn" data-tabid="${t.id}">X</span>
            </div>`;
        });
        html += `</div>`;
    }

    document.getElementById("list").innerHTML = html || '<div style="text-align:center;color:#64748b;padding:20px">No tabs found.</div>';

    // Bind close buttons
    document.querySelectorAll(".close-btn").forEach(btn => {
        btn.addEventListener("click", async (e) => {
            e.stopPropagation();
            const tabId = parseInt(btn.dataset.tabid);
            await chrome.tabs.remove(tabId);
            loadTabs();
        });
    });
}

// === Merge Windows ===
document.getElementById("mergeBtn").addEventListener("click", async () => {
    const tabs = await chrome.tabs.query({});
    if (tabs.length === 0) return;

    // Move all tabs to the first window
    const targetWindow = tabs[0].windowId;
    let moved = 0;
    for (const tab of tabs) {
        if (tab.windowId !== targetWindow) {
            await chrome.tabs.move(tab.id, { windowId: targetWindow, index: -1 });
            moved++;
        }
    }
    await loadTabs();
    alert(`Merged ${moved} tabs into one window.`);
});

// === Sleep Inactive ===
document.getElementById("sleepBtn").addEventListener("click", async () => {
    const now = Date.now();
    const inactiveThreshold = 30 * 60 * 1000; // 30 min
    let count = 0;
    for (const tab of allTabs) {
        if (!tab.active && !tab.discarded) {
            await chrome.tabs.discard(tab.id);
            count++;
        }
    }
    await loadTabs();
    alert(`Slept ${count} inactive tabs to free memory.`);
});

// === Save Session ===
document.getElementById("saveSessionBtn").addEventListener("click", async () => {
    const tabs = await chrome.tabs.query({});
    const session = {
        name: new Date().toLocaleString(),
        tabs: tabs.map(t => ({ url: t.url, title: t.title })),
        date: new Date().toISOString()
    };

    chrome.storage.local.get(["sessions"], (data) => {
        const sessions = data.sessions || [];
        sessions.push(session);
        chrome.storage.local.set({ sessions }, () => {
            alert(`Session "${session.name}" saved with ${tabs.length} tabs.`);
        });
    });
});

// === Show Sessions ===
document.getElementById("sessionsBtn").addEventListener("click", () => {
    showSessions = !showSessions;
    document.getElementById("sessionsBtn").textContent = showSessions ? "Back to Tabs" : "Sessions";
    renderTabs();
});

function renderSessions() {
    chrome.storage.local.get(["sessions"], (data) => {
        const sessions = data.sessions || [];
        if (sessions.length === 0) {
            document.getElementById("list").innerHTML = '<div style="text-align:center;color:#64748b;padding:20px">No saved sessions.</div>';
            return;
        }
        let html = "";
        sessions.forEach((s, i) => {
            html += `<div class="session-row">
                <span>${s.name} (${s.tabs.length} tabs)</span>
                <span class="restore" data-idx="${i}">Restore</span>
            </div>`;
        });
        document.getElementById("list").innerHTML = html;

        document.querySelectorAll(".restore").forEach(btn => {
            btn.addEventListener("click", () => {
                const idx = parseInt(btn.dataset.idx);
                const session = sessions[idx];
                session.tabs.forEach(t => {
                    chrome.tabs.create({ url: t.url, active: false });
                });
            });
        });
    });
}

// Search
document.getElementById("search").addEventListener("input", (e) => {
    searchQuery = e.target.value;
    renderTabs();
});

loadTabs();
