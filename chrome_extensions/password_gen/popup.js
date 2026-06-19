const CHARS = {
    upper: "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    lower: "abcdefghijklmnopqrstuvwxyz",
    numbers: "0123456789",
    symbols: "!@#$%^&*()_+-=[]{}|;:,.<>?"
};

function generate() {
    const length = parseInt(document.getElementById("length").value);
    const useUpper = document.getElementById("upper").checked;
    const useLower = document.getElementById("lower").checked;
    const useNumbers = document.getElementById("numbers").checked;
    const useSymbols = document.getElementById("symbols").checked;

    let pool = "";
    if (useUpper) pool += CHARS.upper;
    if (useLower) pool += CHARS.lower;
    if (useNumbers) pool += CHARS.numbers;
    if (useSymbols) pool += CHARS.symbols;

    if (!pool) {
        document.getElementById("pwdDisplay").textContent = "Select at least one";
        return;
    }

    const arr = new Uint32Array(length);
    crypto.getRandomValues(arr);

    let pwd = "";
    for (let i = 0; i < length; i++) {
        pwd += pool[arr[i] % pool.length];
    }

    const display = document.getElementById("pwdDisplay");
    const bar = document.getElementById("strengthBar");

    display.textContent = pwd;

    // Strength: based on charset size and length
    const entropy = Math.log2(pool.length) * length;
    display.className = "pwd-box";
    bar.className = "strength-bar";
    if (entropy < 60) {
        display.classList.add("weak");
        bar.classList.add("weak");
    } else if (entropy < 80) {
        display.classList.add("medium");
        bar.classList.add("medium");
    } else {
        display.classList.add("strong");
        bar.classList.add("strong");
    }
}

document.getElementById("genBtn").addEventListener("click", generate);

document.getElementById("copyBtn").addEventListener("click", async () => {
    const pwd = document.getElementById("pwdDisplay").textContent;
    if (!pwd || pwd === "Click Generate") return;
    await navigator.clipboard.writeText(pwd);
    const el = document.getElementById("copied");
    el.style.display = "block";
    setTimeout(() => el.style.display = "none", 2000);
});

// Generate on open
generate();
