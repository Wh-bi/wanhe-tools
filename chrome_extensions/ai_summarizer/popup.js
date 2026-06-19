const API = "http://localhost:8888";

document.getElementById("summarizeBtn").addEventListener("click", async () => {
    const btn = document.getElementById("summarizeBtn");
    const loading = document.getElementById("loading");
    const result = document.getElementById("result");
    const output = document.getElementById("output");
    const meta = document.getElementById("meta");
    const model = document.getElementById("model").value;
    const detail = document.getElementById("detail").value;

    btn.disabled = true;
    loading.style.display = "block";
    result.classList.remove("show");

    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        const injection = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: () => document.body.innerText.substring(0, 5000)
        });
        const text = injection[0].result || "";

        if (!text || text.length < 50) {
            output.textContent = "Page too short to summarize.";
            result.classList.add("show");
            return;
        }

        loading.textContent = "Generating summary...";
        const t0 = Date.now();
        const resp = await fetch(`${API}/summarize`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, model, detail })
        });

        if (!resp.ok) {
            output.textContent = `Toolbox error: ${resp.status}. Start toolbox at localhost:8888.`;
            result.classList.add("show");
            return;
        }

        const data = await resp.json();
        const dt = ((Date.now() - t0) / 1000).toFixed(1);

        output.textContent = data.result || "No summary";
        meta.textContent = `Latency: ${dt}s | Model: ${model} | Input: ${text.length} chars`;
        result.classList.add("show");

    } catch (e) {
        output.textContent = `Error: ${e.message}. Start toolbox_backend.py first.`;
        result.classList.add("show");
    } finally {
        btn.disabled = false;
        loading.style.display = "none";
    }
});
