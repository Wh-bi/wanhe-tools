chrome.storage.local.get(["review", "code_snippet"], (data) => {
    if (data.review && data.code_snippet) {
        document.getElementById("empty").style.display = "none";
        document.getElementById("result").style.display = "block";
        document.getElementById("code").textContent = data.code_snippet;
        document.getElementById("body").textContent = data.review;
    }
});
