document.getElementById("enableBtn").addEventListener("click", async () => {
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        // Extract page content
        const injection = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: () => {
                // Try to find main content area
                const selectors = ['article', 'main', '[role="main"]', '.post-content', '.article-content', '#content', '.content'];
                let container = null;
                for (const sel of selectors) {
                    container = document.querySelector(sel);
                    if (container && container.innerText.length > 200) break;
                }
                if (!container) container = document.body;

                // Clone and clean
                const clone = container.cloneNode(true);
                // Remove unwanted elements
                const remove = clone.querySelectorAll('script, style, nav, header, footer, aside, .sidebar, .ad, .advertisement, [class*="ad-"], iframe, .nav, .menu, .comments, .social');
                remove.forEach(el => el.remove());

                return {
                    title: document.title,
                    html: clone.innerHTML.substring(0, 50000)
                };
            }
        });

        const result = injection[0].result;
        if (!result || !result.html) {
            alert("Could not extract page content.");
            return;
        }

        // Store and open reader
        sessionStorage.setItem('reader_content', result.html);
        sessionStorage.setItem('reader_title', result.title);

        // Open reader in new tab
        const readerUrl = chrome.runtime.getURL('reader.html');
        chrome.tabs.create({ url: readerUrl });

    } catch (e) {
        alert("Error: " + e.message);
    }
});
