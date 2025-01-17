from pydantic import BaseModel


class PlagiarismSentence(BaseModel):
    matched_sentence: str
    document_sentence: str
    similarity: float
    index_in_text: int


class AssessmentResponse(BaseModel):
    plagiarisms: list[PlagiarismSentence]
    plagiarisms_other_lang: list[PlagiarismSentence]
    assessment_id: int
    sent_at: str
    rating: float
    rating_other_lang: float
    title: str
    author: str
