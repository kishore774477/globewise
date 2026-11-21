from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def generate_travel_guide():
    return {
        "title": "Demo Travel Guide",
        "summary": "Check weather, carry ID proof, keep emergency contacts ready.",
        "tips": [
            "Check local weather",
            "Keep currency ready",
            "Save emergency numbers",
        ],
    }
