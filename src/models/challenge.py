from pydantic import BaseModel

class AnswerSubmission(BaseModel):
    challenge_id: int
    selected_option: str

class ChallengeCreate(BaseModel):
    title: str
    category: str
    difficulty: str
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    hint: str
    explanation: str