// Load stored translation result when popup opens
chrome.storage.local.get(["translation", "original", "lang"], (data) => {
    if (data.translation && data.original) {
        document.getElementById("empty").style.display = "none";
        document.getElementById("result").style.display = "block";
        document.getElementById("original").textContent = data.original;
        document.getElementById("translation").textContent = data.translation;
    }
});
