async function loadStats() {
    try {
        const res = await fetch('/stats');
        const data = await res.json();
        
        const overallPerc = data.overall?.percentage || 0;
        const overallSolved = data.overall?.solved || 0;
        const overallTotal = data.overall?.total || 0;

        const percElem = document.getElementById('overallPerc');
        const barElem = document.getElementById('overallBar');
        const countsElem = document.getElementById('overallCounts');

        if (percElem) percElem.innerText = `${overallPerc}%`;
        if (barElem) barElem.style.width = `${overallPerc}%`;
        if (countsElem) countsElem.innerText = `${overallSolved} / ${overallTotal} Completed`;
        
        const catContainer = document.getElementById('categoryStatsContainer');
        if (data.categories && catContainer) {
            catContainer.innerHTML = Object.entries(data.categories).map(([cat, stats]) => `
                <div style="margin-bottom: 0.5rem; background: #0f172a; padding: 0.75rem; border-radius: 6px; border: 1px solid #334155;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                        <span style="color: #f8fafc; font-weight: bold;">${cat}</span>
                        <span style="color: #94a3b8;">${stats.solved} / ${stats.total} (${stats.percentage}%)</span>
                    </div>
                    <div style="background: #334155; height: 6px; border-radius: 3px; overflow: hidden;">
                        <div style="background: #0284c7; width: ${stats.percentage}%; height: 100%;"></div>
                    </div>
                </div>
            `).join("");
        }
    } catch (err) {
        console.error("Error loading stats:", err);
    }
}

async function loadLogs() {
    try {
        const res = await fetch('/logs');
        const data = await res.json();
        const tbody = document.getElementById('logsTableBody');
        if (!tbody) return;

        const logsList = data.logs || data;
        if (!Array.isArray(logsList) || logsList.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:#94a3b8; padding: 1rem;">No execution logs found.</td></tr>';
            return;
        }

        tbody.innerHTML = logsList.map(log => `
            <tr>
                <td style="padding: 0.75rem; border-bottom: 1px solid #334155;">#${log.id}</td>
                <td style="padding: 0.75rem; border-bottom: 1px solid #334155;">${log.target}</td>
                <td style="padding: 0.75rem; border-bottom: 1px solid #334155;"><span style="color: ${log.status === 'SUCCESS' ? '#4ade80' : '#f87171'}">${log.status}</span></td>
                <td style="padding: 0.75rem; border-bottom: 1px solid #334155; color: #94a3b8;">${log.timestamp}</td>
            </tr>
        `).join("");
    } catch (err) {
        console.error("Error loading logs:", err);
    }
}

async function clearLogs() {
    try {
        await fetch('/logs', { method: 'DELETE' });
        await loadLogs();
    } catch (e) {
        console.error("Error clearing logs:", e);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadStats();
    loadLogs();

    const clearBtn = document.getElementById("clearBtn");
    if (clearBtn) clearBtn.addEventListener("click", clearLogs);
});