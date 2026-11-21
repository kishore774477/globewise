from fastapi import APIRouter

from app.api.v1.routes import dashboard
from app.api.v1.routes import location
from app.api.v1.routes import weather
from app.api.v1.routes import safety
from app.api.v1.routes import currency
from app.api.v1.routes import translation
from app.api.v1.routes import country_info
from app.api.v1.routes import travel_guide
from app.api.v1.routes import saved_places

api_router = APIRouter()

api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(location.router, prefix="/locations", tags=["Locations"])
api_router.include_router(weather.router, prefix="/weather", tags=["Weather"])
api_router.include_router(safety.router, prefix="/safety", tags=["Safety"])
api_router.include_router(currency.router, prefix="/currency", tags=["Currency"])
api_router.include_router(translation.router, prefix="/translation", tags=["Translation"])
api_router.include_router(country_info.router, prefix="/country-info", tags=["Country Info"])
api_router.include_router(travel_guide.router, prefix="/travel-guide", tags=["Travel Guide"])
api_router.include_router(saved_places.router, prefix="/saved-places", tags=["Saved Places"])
