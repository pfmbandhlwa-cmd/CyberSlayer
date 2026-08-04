import sqlite3

DB_PATH = "cyberslayer.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS execution_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_option TEXT NOT NULL,
            hint TEXT NOT NULL,
            explanation TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            challenge_id INTEGER PRIMARY KEY,
            status TEXT NOT NULL,
            FOREIGN KEY (challenge_id) REFERENCES challenges (id)
        )
    """)

    conn.commit()
    conn.close()
    seed_challenges()

def seed_challenges():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM challenges")
    count = cursor.fetchone()[0]

    if count == 0:
        challenges = [
            (
                "Detecting SQL Injection",
                "Web Security",
                "Beginner",
                "Which HTTP security header specifically prevents a website from being rendered inside an <iframe> tag to protect against Clickjacking?",
                "Content-Security-Policy",
                "X-Frame-Options",
                "Strict-Transport-Security",
                "X-Content-Type-Options",
                "B",
                "Look for the header that directly controls framing behavior.",
                "X-Frame-Options tells the browser whether to allow rendering a page in a <frame>, <iframe>, or <object>."
            ),
            (
                "Understanding Port Scanning",
                "Network Security",
                "Beginner",
                "Which standard TCP port is utilized by default for secure HTTPS encrypted traffic?",
                "Port 80",
                "Port 21",
                "Port 443",
                "Port 8080",
                "C",
                "Port 80 is HTTP, while the secure variant uses a different 400-series port.",
                "Port 443 is the standard port for web traffic encrypted with TLS/SSL (HTTPS)."
            ),
            (
                "Identifying Cryptographic Hashes",
                "Cryptography",
                "Intermediate",
                "Why are simple hash functions like MD5 and SHA-1 considered insecure for storing user passwords?",
                "They take too long to compute.",
                "They are subject to high-speed collision attacks and GPU rainbow tables.",
                "They output variable length strings.",
                "They require a private key to decrypt.",
                "B",
                "Modern GPUs can calculate billions of MD5 hashes per second without salt.",
                "Fast cryptographic hashes like MD5 permit rapid brute-force attacks. Password hashing requires key-derivation algorithms like bcrypt or Argon2."
            ),
            (
                "Analyzing Cross-Site Scripting (XSS)",
                "Web Security",
                "Intermediate",
                "What is the primary objective of a Reflected Cross-Site Scripting (XSS) attack?",
                "Injecting malformed SQL into database forms.",
                "Executing arbitrary JavaScript in the victim's browser context via input echoed back in HTTP responses.",
                "Intercepting raw TCP packets on a local network interface.",
                "Overwhelming the server with SYN requests.",
                "B",
                "XSS targets browser execution rather than server-side execution.",
                "Reflected XSS occurs when untrusted user input is immediately included in a web application's response without proper sanitization."
            )
        ]
        
        cursor.executemany("""
            INSERT INTO challenges 
            (title, category, difficulty, question, option_a, option_b, option_c, option_d, correct_option, hint, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, challenges)
        conn.commit()

    conn.close()

def add_custom_challenge(data: dict) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO challenges 
        (title, category, difficulty, question, option_a, option_b, option_c, option_d, correct_option, hint, explanation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data['title'],
        data['category'],
        data['difficulty'],
        data['question'],
        data['option_a'],
        data['option_b'],
        data['option_c'],
        data['option_d'],
        data['correct_option'].upper(),
        data['hint'],
        data['explanation']
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def get_all_challenges():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id, c.title, c.category, c.difficulty, c.question, 
               c.option_a, c.option_b, c.option_c, c.option_d, c.hint,
               COALESCE(p.status, 'UNANSWERED') as user_status
        FROM challenges c
        LEFT JOIN user_progress p ON c.id = p.challenge_id
        ORDER BY c.id ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def check_challenge_answer(challenge_id: int, selected_option: str) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT correct_option, explanation FROM challenges WHERE id = ?", (challenge_id,))
    challenge = cursor.fetchone()

    if not challenge:
        conn.close()
        return {"status": "ERROR", "message": "Challenge not found"}

    is_correct = challenge["correct_option"].upper() == selected_option.upper()
    status_text = "SOLVED" if is_correct else "FAILED"

    cursor.execute("""
        INSERT INTO user_progress (challenge_id, status)
        VALUES (?, ?)
        ON CONFLICT(challenge_id) DO UPDATE SET status = excluded.status
    """, (challenge_id, status_text))
    
    conn.commit()
    conn.close()

    return {
        "correct": is_correct,
        "correct_option": challenge["correct_option"],
        "explanation": challenge["explanation"]
    }

def clear_all_logs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM execution_logs")
    conn.commit()
    conn.close()

def log_execution(target: str, status: str, timestamp: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO execution_logs (target, status, timestamp)
        VALUES (?, ?, ?)
    """, (target, status, timestamp))
    conn.commit()
    conn.close()

def get_all_logs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM execution_logs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_challenge_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Overall total and solved
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN p.status = 'SOLVED' THEN 1 ELSE 0 END) as solved
        FROM challenges c
        LEFT JOIN user_progress p ON c.id = p.challenge_id
    """)
    overall = cursor.fetchone()
    total = overall['total'] or 0
    solved = overall['solved'] or 0
    overall_percentage = round((solved / total) * 100) if total > 0 else 0

    # Category breakdown
    cursor.execute("""
        SELECT 
            c.category,
            COUNT(*) as total,
            SUM(CASE WHEN p.status = 'SOLVED' THEN 1 ELSE 0 END) as solved
        FROM challenges c
        LEFT JOIN user_progress p ON c.id = p.challenge_id
        GROUP BY c.category
    """)
    rows = cursor.fetchall()
    conn.close()

    categories = {}
    for row in rows:
        cat_total = row['total']
        cat_solved = row['solved'] or 0
        categories[row['category']] = {
            "total": cat_total,
            "solved": cat_solved,
            "percentage": round((cat_solved / cat_total) * 100) if cat_total > 0 else 0
        }

    return {
        "overall": {
            "total": total,
            "solved": solved,
            "percentage": overall_percentage
        },
        "categories": categories
    }
