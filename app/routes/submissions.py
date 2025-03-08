from fastapi import APIRouter, Depends
from app.utils.code_runner import execute_code
from app.schemas.submission_schema import CodeSubmission

router = APIRouter()

@router.post("/execute")
def execute_code_submission(submission: CodeSubmission):
    result = execute_code(submission.code)
    return result