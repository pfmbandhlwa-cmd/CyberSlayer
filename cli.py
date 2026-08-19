import sys
from src.services.ai_service import ai_service

# Temporary CLI session state
user_profile = {"username": "CyberSlayer", "score": 0, "solved": set()}

CHALLENGES = {
    1: {
        "title": "SQLi Auth Bypass",
        "category": "sqli",
        "points": 100,
        "flag": "cyber{sqli_bypass}",
        "desc": "Bypass login via vulnerable SQL input.",
        "attempts": 0
    },
    2: {
        "title": "Reflected XSS Portal",
        "category": "xss",
        "points": 250,
        "flag": "cyber{xss_reflected}",
        "desc": "Inject executable script in query param.",
        "attempts": 0
    },
    3: {
        "title": "Base64 Header Secret",
        "category": "crypto",
        "points": 100,
        "flag": "cyber{b64_secret}",
        "desc": "Extract and decode server header token.",
        "attempts": 0
    }
}

def display_menu():
    print("\n" + "="*40)
    print(f" 🗡️  CYBERSLAYER CLI | Score: {user_profile['score']} PTS")
    print("="*40)
    print("[1] View Active Challenges")
    print("[2] Submit Challenge Flag")
    print("[3] Ask AI Mentor for Hint")
    print("[4] View Profile & Stats")
    print("[5] Exit")
    print("="*40)

def list_challenges():
    print("\n--- AVAILABLE CHALLENGES ---")
    for cid, ch in CHALLENGES.items():
        status = "✅ SOLVED" if cid in user_profile["solved"] else f"🔒 {ch['points']} PTS"
        print(f"[{cid}] {ch['title']} ({ch['category'].upper()}) - {status}")
        print(f"    {ch['desc']}")

def submit_flag():
    list_challenges()
    try:
        cid = int(input("\nEnter Challenge ID to submit flag: "))
        if cid not in CHALLENGES:
            print("❌ Invalid Challenge ID.")
            return

        if cid in user_profile["solved"]:
            print("⚠️ You already solved this challenge!")
            return

        ch = CHALLENGES[cid]
        flag_input = input(f"Enter flag for '{ch['title']}': ").strip()

        if flag_input == ch["flag"]:
            user_profile["score"] += ch["points"]
            user_profile["solved"].add(cid)
            print(f"\n🎉 CORRECT! You earned +{ch['points']} PTS!")
        else:
            ch["attempts"] += 1
            print("\n❌ Incorrect flag.")
            # Auto-suggest AI feedback on failed attempt
            feedback = ai_service.analyze_attempt(ch["title"], flag_input, ch["category"])
            print(f"💡 AI Mentor Feedback: {feedback['feedback']}")
    except ValueError:
        print("❌ Please enter a valid number.")

def request_hint():
    list_challenges()
    try:
        cid = int(input("\nEnter Challenge ID for a hint: "))
        if cid not in CHALLENGES:
            print("❌ Invalid Challenge ID.")
            return

        ch = CHALLENGES[cid]
        ch["attempts"] += 1
        hint_data = ai_service.generate_hint(
            challenge_title=ch["title"],
            category=ch["category"],
            attempt_count=ch["attempts"]
        )
        print(f"\n{hint_data['hint']}")
    except ValueError:
        print("❌ Please enter a valid number.")

def view_profile():
    print("\n--- USER PROFILE ---")
    print(f"Username:       {user_profile['username']}")
    print(f"Total Score:    {user_profile['score']} PTS")
    print(f"Solved Count:   {len(user_profile['solved'])} / {len(CHALLENGES)}")
    rank = "Novice" if user_profile["score"] < 200 else "Cyber Slayer"
    print(f"Current Rank:   {rank}")

def main():
    while True:
        display_menu()
        choice = input("Select an option (1-5): ").strip()
        
        if choice == "1":
            list_challenges()
        elif choice == "2":
            submit_flag()
        elif choice == "3":
            request_hint()
        elif choice == "4":
            view_profile()
        elif choice == "5":
            print("\nGoodbye, CyberSlayer!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
