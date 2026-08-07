document.addEventListener("DOMContentLoaded", () => {
    loadUserChallenges();
});

async function loadUserChallenges() {
    const container = document.getElementById("challenges-grid") || document.getElementById("challenges-container");
    if (!container) return;

    try {
        const response = await fetch("/challenges/");
        const data = await response.json();

        if (!data.challenges || data.challenges.length === 0) {
            container.innerHTML = "<p>No active challenges available.</p>";
            return;
        }

        container.innerHTML = data.challenges.map(item => `
            <div class="challenge-card difficulty-${item.difficulty.toLowerCase()}">
                <div class="card-header">
                    <h3>${item.title}</h3>
                    <span class="badge ${item.category}">${item.category.toUpperCase()}</span>
                </div>
                <p class="description">${item.description}</p>
                <div class="card-footer">
                    <span class="points">+${item.points} PTS</span>
                    <button onclick="openSubmissionModal(${item.id})">Solve Challenge</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error("Failed to load challenges:", error);
    }
}

async function submitFlag(challengeId, inputFlag) {
    try {
        const response = await fetch(`/challenges/${challengeId}/submit`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ flag: inputFlag })
        });
        const result = await response.json();
        alert(result.message);
    } catch (error) {
        console.error("Submission error:", error);
    }
}
