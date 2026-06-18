from fastapi import APIRouter

from app.services.overpass_service import (
    get_nearby_places
)

from app.recommender.ranking import (
    rank_places
)

router = APIRouter()

@router.get("/places")
def places(
    lat: float,
    lon: float,
    radius: int = 3000,
    occasion: str = "friends",
    budget: int = 1000,
    cuisine: str = "",
    ambience: str = ""
):

    results = get_nearby_places(
        lat,
        lon,
        radius
    )

    if "places" not in results:
        return {
            "occasion": occasion,
            "count": 0,
            "recommendations": []
        }

    recommendations = rank_places(
        lat,
        lon,
        results["places"],
        occasion,
        budget,
        cuisine,
        ambience
    )

    return {

        "occasion": occasion,

        "budget": budget,

        "cuisine": cuisine,

        "ambience": ambience,

        "count":
        len(recommendations),

        "recommendations":
        recommendations
    }