from src.database.db import get_all_challenges_db
from src.database.db import check_challenge_answer, add_custom_challenge, get_challenge_stats

class ChallengeService:
    def list_challenges(self):
        return get_all_challenges_db()

    def get_stats(self):
        return get_challenge_stats()

    def create(self, challenge_data: dict):
        return add_custom_challenge(challenge_data)

    def verify_answer(self, challenge_id: int, selected_option: str):
        return check_challenge_answer(challenge_id, selected_option)

challenge_service = ChallengeService()