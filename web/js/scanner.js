async function runScan() {
    const targetInput = document.getElementById("targetInput");
    const output = document.getElementById("output");
    
    if (!targetInput || !output) return;

    const target = targetInput.value;
    output.style.display = "block";
    output.innerText = `Running scan against ${target}...`;

    try {
        const res = await fetch('/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target })
        });
        const data = await res.json();
        output.innerText = JSON.stringify(data, null, 2);
        if (typeof loadLogs === "function") loadLogs();
    } catch (e) {
        output.innerText = `Scan failed: ${e}`;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const runBtn = document.getElementById("runBtn");
    if (runBtn) runBtn.addEventListener("click", runScan);
});