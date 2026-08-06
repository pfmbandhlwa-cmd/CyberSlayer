async function loadChallenges() {
    const container = document.getElementById("challengesContainer");
    if (!container) return;

    try {
        const res = await fetch("/challenges");
        const data = await res.json();
        const items = data.challenges || data;

        if (!Array.isArray(items) || items.length === 0) {
            container.innerHTML = "<p>No challenges available.</p>";
            return;
        }

        container.innerHTML = items.map(item => `
            <div class="challenge-card" id="challenge-${item.id}">
                <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.5rem;">
                    <span style="background: #0284c7; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.8rem; color: #fff;">${item.category}</span>
                    <span style="background: #334155; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.8rem; color: #fff;">${item.difficulty}</span>
                    ${item.user_status === "SOLVED" ? '<span style="background: #166534; color: #dcfce7; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.8rem; margin-left:auto;">✔ SOLVED</span>' : ''}
                    ${item.user_status === "FAILED" ? '<span style="background: #991b1b; color: #fee2e2; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.8rem; margin-left:auto;">✖ ATTEMPTED</span>' : ''}
                </div>
                <h3 style="margin-top:0.8rem; margin-bottom:0.4rem; color: #f8fafc;">#${item.id}. ${item.title}</h3>
                <p style="color:#e2e8f0; margin-bottom: 1rem;">${item.question}</p>
                <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1rem;">
                    <label style="color: #cbd5e1; cursor: pointer;"><input type="radio" name="challenge_${item.id}" value="A"> A) ${item.option_a}</label>
                    <label style="color: #cbd5e1; cursor: pointer;"><input type="radio" name="challenge_${item.id}" value="B"> B) ${item.option_b}</label>
                    <label style="color: #cbd5e1; cursor: pointer;"><input type="radio" name="challenge_${item.id}" value="C"> C) ${item.option_c}</label>
                    <label style="color: #cbd5e1; cursor: pointer;"><input type="radio" name="challenge_${item.id}" value="D"> D) ${item.option_d}</label>
                </div>
                <div style="display: flex; gap: 1rem; align-items: center;">
                    <button onclick="submitAnswer(${item.id})" style="background: #2563eb; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; font-weight: bold;">Submit Answer</button>
                    <button onclick="alert('Hint: ' + ${JSON.stringify(item.hint)})" style="background: transparent; border: 1px solid #64748b; color: #94a3b8; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer;">💡 Hint</button>
                </div>
                <div id="result_${item.id}" style="margin-top: 10px; border-radius: 5px; display: none;"></div>
            </div>
        `).join("");
    } catch (err) {
        container.innerHTML = '<p style="color: #ef4444;">Error loading challenges from server.</p>';
    }
}

async function submitAnswer(challengeId) {
    const selected = document.querySelector(`input[name="challenge_${challengeId}"]:checked`);
    const resDiv = document.getElementById(`result_${challengeId}`);
    
    if (!selected) {
        alert("Please select an option first!");
        return;
    }

    try {
        const response = await fetch(`/challenges/${challengeId}/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ selected_option: selected.value })
        });
        const result = await response.json();
        resDiv.style.display = "block";
        
        if (result.correct) {
            resDiv.style.background = "#14532d";
            resDiv.style.color = "#86efac";
            resDiv.style.padding = "0.75rem";
            resDiv.innerHTML = `<strong>✔ Correct!</strong> ${result.explanation}`;
        } else {
            resDiv.style.background = "#7f1d1d";
            resDiv.style.color = "#fca5a5";
            resDiv.style.padding = "0.75rem";
            resDiv.innerHTML = `<strong>✖ Incorrect.</strong> ${result.explanation}`;
        }

        if (typeof loadStats === "function") loadStats();
        loadChallenges();
    } catch (e) {
        console.error("Submission error:", e);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadChallenges();
});