from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def translate_text():
    return {
        "source_text": "Hello",
        "translated_text": "Hola",
        "source_language": "en",
        "target_language": "es",
    }
