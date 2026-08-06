import os
from typing import Optional, Dict, Any

class AIService:
    """
    AI Mentor Service for CyberSlayer.
    Generates dynamic cybersecurity hints, analyzes failed attempts,
    and provides contextual CTF guidance.
    """

    HINT_CATALOG = {
        "web": [
            "Examine input validation and client-side sanitization mechanisms.",
            "Inspect HTTP request headers, hidden form fields, and response cookies.",
            "Look for unhandled edge cases in parameters or API payloads."
        ],
        "sqli": [
            "Test input fields with single quotes (') or double quotes (\") to induce database syntax errors.",
            "Attempt boolean-based logical conditions (e.g., ' OR 1=1 --) to modify query logic.",
            "Use UNION SELECT queries to extract table schemas and database contents."
        ],
        "xss": [
            "Locate where user input is reflected into the DOM without HTML entity encoding.",
            "Test basic execution vectors like <script>alert(1)</script> or event handlers (e.g., onerror=).",
            "Try attribute breakouts (e.g., \" onfocus=\"alert(1)) if direct tag insertion is blocked."
        ],
        "crypto": [
            "Identify whether the data is encoded (Base64, Hex) or actually encrypted (AES, RSA).",
            "Perform frequency analysis or cipher key length checks for classic substitution ciphers.",
            "Check for fixed initialization vectors (IVs) or weak key generation routines."
        ],
        "forensics": [
            "Verify file headers and magic bytes using 'file' or 'hexdump' utilities.",
            "Inspect embedded image or binary metadata using 'exiftool' or 'strings'.",
            "Analyze trailing bytes at the end of files for hidden archived payloads."
        ],
        "network": [
            "Filter packet captures (.pcap) in Wireshark for cleartext protocols like HTTP, FTP, or DNS.",
            "Inspect TCP handshake flags and stream reassembly for hidden payload transfers.",
            "Look for non-standard port traffic or covert timing channels."
        ]
    }

    def generate_hint(
        self, 
        challenge_title: str, 
        category: str, 
        difficulty: str = "Medium", 
        attempt_count: int = 1
    ) -> Dict[str, Any]:
        """Returns progressive hints based on category and current attempt count."""
        cat_key = category.lower().strip()
        hints = self.HINT_CATALOG.get(cat_key, [
            "Analyze target behavior step-by-step and monitor system outputs.",
            "Review core protocol specifications and implementation standards."
        ])
        
        # Progressive indexing based on total failed attempts
        hint_index = min(max(attempt_count - 1, 0), len(hints) - 1)
        selected_hint = hints[hint_index]

        return {
            "challenge": challenge_title,
            "category": category,
            "difficulty": difficulty,
            "hint_level": hint_index + 1,
            "max_hints": len(hints),
            "hint": f"[{category.upper()} - Hint Level {hint_index + 1}]: {selected_hint}"
        }

    def analyze_attempt(self, challenge_title: str, user_submission: str, category: str) -> Dict[str, Any]:
        """Provides feedback on an incorrect flag or payload submission."""
        submission_clean = user_submission.strip()
        
        if not submission_clean:
            feedback = "Empty submission received. Enter a candidate payload or flag format."
        elif "flag{" in submission_clean.lower() or "cyber{" in submission_clean.lower():
            feedback = "Flag wrapper format recognized, but the inner hash/token is incorrect."
        else:
            feedback = f"Payload rejected. Review standard {category} exploit syntax."

        hint_data = self.generate_hint(challenge_title, category, attempt_count=1)
        
        return {
            "status": "incorrect",
            "feedback": feedback,
            "suggested_hint": hint_data["hint"]
        }

    def get_mentor_response(self, prompt: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Handles conversational AI Mentor chat requests."""
        cleaned_prompt = prompt.strip()
        if not cleaned_prompt:
            return {"reply": "How can I assist you with your security challenge today?"}

        # Context-aware guidance output
        reply = (
            f"**AI Mentor:** To tackle '{cleaned_prompt}', break the process into "
            f"reconnaissance, target identification, and payload validation."
        )
        if context:
            reply += f" Context focus: {context}."

        return {"reply": reply, "context": context}

ai_service = AIService()
