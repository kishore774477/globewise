from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_saved_places():
    return {
        "saved_places": [],
    }
