from src.database.db import engine, Base, SessionLocal
from src.models.challenge import Challenge

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(Challenge).first() is None:
        initial_challenges = [
            Challenge(
                title="SQLi Authentication Bypass",
                category="sqli",
                difficulty="Easy",
                points=100,
                description="Bypass the login authentication mechanism by manipulating SQL parameters.",
                flag="cyber{sqli_admin_bypass_2026}"
            ),
            Challenge(
                title="Reflected XSS Search Parameter",
                category="xss",
                difficulty="Medium",
                points=250,
                description="Inject an executable script payload into the unencoded search query string.",
                flag="cyber{xss_dom_reflection_success}"
            ),
            Challenge(
                title="Base64 Header Secret",
                category="crypto",
                difficulty="Easy",
                points=100,
                description="Extract and decode the encoded authorization token stored in the server headers.",
                flag="cyber{b64_header_decoded_flag}"
            )
        ]
        db.add_all(initial_challenges)
        db.commit()
        print("Database seeded with default challenges.")
    else:
        print("Database already contains data. Skipping seed.")

    db.close()

if __name__ == "__main__":
    seed_database()
