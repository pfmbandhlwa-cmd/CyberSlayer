async function createChallenge(e) {
    e.preventDefault();
    const payload = {
        title: document.getElementById("newTitle").value,
        category: document.getElementById("newCategory").value,
        difficulty: document.getElementById("newDifficulty").value,
        question: document.getElementById("newQuestion").value,
        option_a: document.getElementById("newOptionA").value,
        option_b: document.getElementById("newOptionB").value,
        option_c: document.getElementById("newOptionC").value,
        option_d: document.getElementById("newOptionD").value,
        correct_option: document.getElementById("newCorrectOption").value,
        hint: document.getElementById("newHint").value,
        explanation: document.getElementById("newExplanation").value
    };

    try {
        const res = await fetch('/challenges', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            alert("Challenge added successfully!");
            document.getElementById("addChallengeForm").reset();
            document.getElementById("adminPanel").style.display = "none";
            if (typeof loadChallenges === "function") loadChallenges();
            if (typeof loadStats === "function") loadStats();
        } else {
            alert("Failed to add challenge.");
        }
    } catch (err) {
        console.error("Error adding challenge:", err);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const toggleAdminBtn = document.getElementById("toggleAdminBtn");
    if (toggleAdminBtn) {
        toggleAdminBtn.addEventListener("click", () => {
            const panel = document.getElementById("adminPanel");
            if (panel) panel.style.display = panel.style.display === "block" ? "none" : "block";
        });
    }

    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            alert("Logged out from admin session.");
        });
    }

    const addChallengeForm = document.getElementById("addChallengeForm");
    if (addChallengeForm) addChallengeForm.addEventListener("submit", createChallenge);
});