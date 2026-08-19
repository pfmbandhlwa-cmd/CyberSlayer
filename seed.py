from src.database.db import get_connection, create_tables


def seed_challenges():
    create_tables()
    connection = get_connection()

    challenges = [
        (
            "Phishing Basics",
            "What is the main goal of a phishing attack?",
            "Improve network speed",
            "Trick users into revealing sensitive information",
            "Encrypt a database",
            "Scan open ports",
            "B",
            "Social Engineering",
            "Beginner",
            10
        ),
        (
            "HTTPS",
            "What does HTTPS primarily provide?",
            "Faster internet",
            "Encrypted communication between a browser and server",
            "More storage",
            "Protection from all malware",
            "B",
            "Web Security",
            "Beginner",
            10
        ),
        (
            "SQL Injection",
            "What type of vulnerability allows malicious SQL to be inserted into a query?",
            "SQL Injection",
            "Cross-Site Scripting",
            "Phishing",
            "DDoS",
            "A",
            "Web Security",
            "Beginner",
            10
        ),
        (
            "Firewalls",
            "What is the primary purpose of a firewall?",
            "Store passwords",
            "Filter and control network traffic",
            "Create websites",
            "Encrypt files",
            "B",
            "Network Security",
            "Beginner",
            10
        ),
        (
            "MFA",
            "What does MFA stand for?",
            "Multiple File Access",
            "Multi-Factor Authentication",
            "Managed Firewall Application",
            "Malware Filtering Application",
            "B",
            "Authentication",
            "Beginner",
            10
        )
    ]

    for challenge in challenges:
        connection.execute("""
            INSERT OR IGNORE INTO challenges (
                title,
                question,
                option_a,
                option_b,
                option_c,
                option_d,
                correct_answer,
                category,
                difficulty,
                points
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, challenge)

    connection.commit()
    connection.close()
    print("✅ Challenges seeded successfully!")


if __name__ == "__main__":
    seed_challenges()
