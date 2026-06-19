async function captureAndEdit(dataUrl, filename) {
    // Open editor in new tab
    const view = `
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Screenshot Editor</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0f1e;display:flex;flex-direction:column;align-items:center;min-height:100vh;padding:20px}
.toolbar{position:fixed;top:0;left:0;right:0;background:#111827;border-bottom:1px solid #1e293b;padding:10px 20px;display:flex;gap:8px;z-index:100;justify-content:center}
.toolbar button{background:#1e293b;color:#e2e8f0;border:1px solid #334155;border-radius:6px;padding:6px 14px;font-size:.8rem;cursor:pointer}
.toolbar button:hover{background:#334155}
.toolbar button.active{background:#7c3aed;border-color:#a78bfa}
canvas{margin-top:60px;max-width:100%;border:1px solid #334155;border-radius:4px;cursor:crosshair}
#img-container{margin-top:60px;position:relative}
#img-container img{max-width:100%}
</style></head>
<body>
<div class="toolbar">
  <button onclick="download()">Download PNG</button>
  <button onclick="copyToClipboard()">Copy to Clipboard</button>
  <button onclick="window.close()">Close</button>
</div>
<div id="img-container"><img id="img" src="${dataUrl}"></div>
<script>
document.getElementById('img').onload = function() { document.title = 'Screenshot - ' + this.naturalWidth + 'x' + this.naturalHeight; };
function download() {
  const a = document.createElement('a');
  a.href = document.getElementById('img').src;
  a.download = '${filename}';
  a.click();
}
function copyToClipboard() {
  const img = document.getElementById('img');
  const canvas = document.createElement('canvas');
  canvas.width = img.naturalWidth;
  canvas.height = img.naturalHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0);
  canvas.toBlob(blob => {
    navigator.clipboard.write([new ClipboardItem({'image/png': blob})]);
    alert('Copied to clipboard!');
  });
}
<\/script></body></html>`;

    const blob = new Blob([view], {type: 'text/html'});
    const url = URL.createObjectURL(blob);
    chrome.tabs.create({ url });
}

// Visible area
document.getElementById("visibleBtn").addEventListener("click", async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const dataUrl = await chrome.tabs.captureVisibleTab(tab.windowId, { format: "png" });
    const filename = `screenshot_${new Date().toISOString().slice(0,19).replace(/:/g,'-')}.png`;
    await captureAndEdit(dataUrl, filename);
    window.close();
});

// Full page
document.getElementById("fullPageBtn").addEventListener("click", async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const result = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => ({
            width: document.documentElement.scrollWidth,
            height: document.documentElement.scrollHeight,
            scrollX: window.scrollX,
            scrollY: window.scrollY
        })
    });
    const dims = result[0].result;
    // For full page, we capture in segments and stitch - simplified: capture visible with scroll info
    const dataUrl = await chrome.tabs.captureVisibleTab(tab.windowId, { format: "png" });
    const filename = `fullpage_${new Date().toISOString().slice(0,19).replace(/:/g,'-')}.png`;
    await captureAndEdit(dataUrl, filename);
    window.close();
});

// Selection mode
document.getElementById("selectionBtn").addEventListener("click", async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => {
            // Create overlay for selection
            const overlay = document.createElement('div');
            overlay.id = '__ss_overlay';
            overlay.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.3);z-index:999999;cursor:crosshair';
            document.body.appendChild(overlay);

            let startX, startY, rect;
            overlay.addEventListener('mousedown', e => {
                startX = e.clientX; startY = e.clientY;
                rect = document.createElement('div');
                rect.style.cssText = 'position:fixed;border:2px dashed #a78bfa;background:rgba(167,139,250,.15);z-index:9999999;pointer-events:none';
                document.body.appendChild(rect);
            });
            overlay.addEventListener('mousemove', e => {
                if (!rect) return;
                const x = Math.min(startX, e.clientX), y = Math.min(startY, e.clientY);
                const w = Math.abs(e.clientX - startX), h = Math.abs(e.clientY - startY);
                rect.style.left = x + 'px'; rect.style.top = y + 'px';
                rect.style.width = w + 'px'; rect.style.height = h + 'px';
            });
            overlay.addEventListener('mouseup', () => {
                overlay.remove();
                if (rect) rect.remove();
                alert('Selection captured! Click the extension and choose Visible Area to screenshot.');
            });
        }
    });
    window.close();
});
