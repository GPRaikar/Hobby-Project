"""SMS parser router for parsing bank SMS messages."""
from typing import List
from fastapi import APIRouter, Body
from app.services.sms_parser import parse_sms, parse_multiple_sms

router = APIRouter(prefix="/sms", tags=["SMS Parser"])


@router.post("/parse")
def parse_single_sms(sms_text: str = Body(..., embed=True)):
    """Parse a single SMS message."""
    result = parse_sms(sms_text)
    return result.to_dict()


@router.post("/parse-bulk")
def parse_bulk_sms(sms_list: List[str] = Body(...)):
    """Parse multiple SMS messages."""
    results = parse_multiple_sms(sms_list)
    return [result.to_dict() for result in results]
