from src.database.db import get_connection, create_tables


def seed_challenges():
    create_tables()
    connection = get_connection()

    challenges = [
        # --- BEGINNER (10 PTS) ---
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
            10,
            "Phishing uses social engineering tactics to manipulate individuals into disclosing personal information like credentials or banking details."
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
            10,
            "HTTPS leverages TLS/SSL protocols to encrypt traffic in transit, preventing eavesdropping and tampered network data."
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
            10,
            "SQL Injection occurs when unsanitized user input is concatenated directly into SQL queries, altering command execution."
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
            10,
            "Firewalls monitor and enforce security policies on incoming and outgoing network traffic based on predefined rules."
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
            10,
            "Multi-Factor Authentication requires two or more verification factors to gain access, drastically improving security over password-only logins."
        ),

        # --- MEDIUM (25 PTS) ---
        (
            "Stored XSS",
            "Which type of XSS attack executes malicious script directly from the backend database where it was permanently saved?",
            "Stored XSS",
            "Reflected XSS",
            "DOM-based XSS",
            "Blind SQLi",
            "A",
            "Web Security",
            "Medium",
            25,
            "Stored (Persistent) XSS occurs when an application stores untrusted user input without sanitization and renders it to subsequent users."
        ),
        (
            "Asymmetric Encryption",
            "Which of the following encryption algorithms relies on a public and private key pair?",
            "AES-256",
            "DES",
            "RSA",
            "Blowfish",
            "C",
            "Cryptography",
            "Medium",
            25,
            "RSA is an asymmetric algorithm using asymmetric key pairs (Public for encryption, Private for decryption), unlike symmetric ciphers like AES."
        ),
        (
            "TCP Handshake",
            "During a standard TCP 3-way handshake, what packet is sent second by the server back to the client?",
            "SYN",
            "SYN-ACK",
            "ACK",
            "FIN-ACK",
            "B",
            "Network Security",
            "Medium",
            25,
            "The 3-way handshake sequence is Client SYN -> Server SYN-ACK -> Client ACK to establish a reliable stateful connection."
        ),
        (
            "JWT Structure",
            "What are the three dot-separated components of a JSON Web Token (JWT)?",
            "Header.Payload.Signature",
            "Key.IV.Ciphertext",
            "User.Role.Permission",
            "Version.Digest.Key",
            "A",
            "Authentication",
            "Medium",
            25,
            "A JWT consists of three Base64URL-encoded parts: the Header (algorithm/type), Payload (claims), and Signature (verification hash)."
        ),

        # --- HARD (50 PTS) ---
        (
            "ASLR Memory Protection",
            "Which OS mechanism randomizes process memory layout addresses to prevent ROP and buffer overflow exploits?",
            "DEP",
            "ASLR",
            "Stack Canary",
            "SEH",
            "B",
            "Memory Exploitation",
            "Hard",
            50,
            "Address Space Layout Randomization (ASLR) randomizes memory positions for key data areas (stack, heap, libraries) to prevent reliable address targeting."
        ),
        (
            "SameSite Cookie Attribute",
            "Which cookie flag restricts browser submission on cross-site requests to prevent CSRF attacks?",
            "HttpOnly",
            "Secure",
            "SameSite",
            "Domain",
            "C",
            "Web Security",
            "Hard",
            50,
            "The SameSite flag (Strict/Lax) instructs browsers whether to attach cookies during cross-site requests, directly mitigating CSRF."
        ),
        (
            "Kerberoasting",
            "Which Active Directory technique requests TGS service tickets for accounts with SPNs to crack hashes offline?",
            "Pass-the-Hash",
            "Kerberoasting",
            "DCSync",
            "Golden Ticket",
            "B",
            "Active Directory",
            "Hard",
            50,
            "Kerberoasting allows authenticated domain users to request TGS tickets for SPNs and perform offline brute-force cracking against service account passwords."
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
                points,
                explanation
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, challenge)

    connection.commit()
    connection.close()
    print("✅ Challenges seeded with Beginner, Medium, and Hard questions!")


if __name__ == "__main__":
    seed_challenges()
