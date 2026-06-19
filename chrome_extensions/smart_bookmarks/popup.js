const API = "http://localhost:8888";
let allBookmarks = [];
let searchQuery = "";

// Load all bookmarks on open
chrome.bookmarks.getTree((tree) => {
    allBookmarks = flattenTree(tree);
    renderStats();
    renderList();
});

function flattenTree(nodes) {
    let result = [];
    for (const n of nodes) {
        if (n.url) result.push({ title: n.title, url: n.url, id: n.id, parentId: n.parentId, isDead: false, isDup: false });
        if (n.children) result = result.concat(flattenTree(n.children));
    }
    return result;
}

// Render statistics
function renderStats() {
    const cats = new Set();
    allBookmarks.forEach(b => cats.add(b.category || "Uncategorized"));
    const dead = allBookmarks.filter(b => b.isDead).length;
    document.getElementById("stats").innerHTML =
        `Total: <span>${allBookmarks.length}</span> | Categories: <span>${cats.size}</span> | Dead: <span style="color:#ef4444">${dead}</span>`;
}

// Render list
function renderList() {
    const q = searchQuery.toLowerCase();
    let filtered = allBookmarks;
    if (q) {
        filtered = allBookmarks.filter(b =>
            (b.title || "").toLowerCase().includes(q) || (b.url || "").toLowerCase().includes(q)
        );
    }

    // Group by category
    const groups = {};
    filtered.forEach(b => {
        const cat = b.category || "Uncategorized";
        if (!groups[cat]) groups[cat] = [];
        groups[cat].push(b);
    });

    let html = "";
    for (const [cat, items] of Object.entries(groups)) {
        html += `<div class="category">`;
        html += `<div class="cat-header" onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display==='none'?'block':'none'">
            <span>${cat}</span><span class="count">${items.length}</span></div>`;
        html += `<div class="cat-items">`;
        items.forEach(b => {
            let tags = "";
            if (b.isDead) tags += '<span class="dead">DEAD</span>';
            if (b.isDup) tags += '<span class="dup">DUP</span>';
            html += `<div class="bookmark">
                <a href="${b.url}" target="_blank" title="${b.url}">${b.title || b.url}</a>${tags}
            </div>`;
        });
        html += `</div></div>`;
    }

    if (filtered.length === 0) {
        html = '<div style="text-align:center;color:#64748b;padding:20px">No bookmarks found.</div>';
    }

    document.getElementById("list").innerHTML = html;
}

// === AI Classification ===
document.getElementById("classifyBtn").addEventListener("click", async () => {
    const btn = document.getElementById("classifyBtn");
    const loading = document.getElementById("loading");
    btn.disabled = true;
    loading.style.display = "block";

    try {
        const bookmarks = allBookmarks.map(b => ({ title: b.title, url: b.url }));
        const resp = await fetch(`${API}/classify`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ bookmarks })
        });
        const data = await resp.json();

        if (data.categories) {
            // Apply categories
            const idxMap = {};
            allBookmarks.forEach((b, i) => idxMap[i] = b);
            for (const [cat, indices] of Object.entries(data.categories)) {
                indices.forEach(i => {
                    if (allBookmarks[i]) allBookmarks[i].category = cat;
                });
            }
        }
        renderStats();
        renderList();
    } catch (e) {
        alert("AI classification error: " + e.message);
    } finally {
        btn.disabled = false;
        loading.style.display = "none";
    }
});

// === Deduplication ===
document.getElementById("dedupeBtn").addEventListener("click", async () => {
    const seen = new Map();
    const dups = [];
    allBookmarks.forEach(b => {
        if (seen.has(b.url)) {
            dups.push(b);
        } else {
            seen.set(b.url, b);
        }
    });

    if (dups.length === 0) {
        alert("No duplicate bookmarks found.");
        return;
    }

    if (confirm(`Found ${dups.length} duplicate bookmarks. Remove them?`)) {
        let removed = 0;
        for (const dup of dups) {
            try {
                await chrome.bookmarks.remove(dup.id);
                removed++;
            } catch (e) { /* skip */ }
        }
        // Reload
        chrome.bookmarks.getTree((tree) => {
            allBookmarks = flattenTree(tree);
            renderStats();
            renderList();
        });
        alert(`Removed ${removed} duplicates.`);
    }
});

// === Dead Link Detection ===
document.getElementById("deadBtn").addEventListener("click", async () => {
    const btn = document.getElementById("deadBtn");
    const loading = document.getElementById("loading");
    btn.disabled = true;
    loading.style.display = "block";

    let checked = 0;
    let dead = 0;

    // Check in batches of 5
    for (let i = 0; i < allBookmarks.length; i += 5) {
        const batch = allBookmarks.slice(i, i + 5);
        await Promise.all(batch.map(async (b) => {
            try {
                const resp = await fetch(b.url, { method: "HEAD", mode: "no-cors" });
                checked++;
            } catch (e) {
                b.isDead = true;
                dead++;
                checked++;
            }
        }));
        // Update progress
        document.getElementById("loading").textContent = `Checking... ${Math.min(i+5, allBookmarks.length)}/${allBookmarks.length}`;
    }

    renderStats();
    renderList();
    btn.disabled = false;
    document.getElementById("loading").style.display = "none";
    alert(`Checked ${checked} links. Found ${dead} dead links.`);
});
