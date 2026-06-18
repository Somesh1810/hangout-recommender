from geopy.distance import geodesic

from app.utils.place_profiles import (
    PLACE_PROFILES
)

def rank_places(
    user_lat,
    user_lon,
    places,
    occasion,
    budget=None,
    cuisine=None,
    ambience=None
):

    ranked = []

    for place in places:

        distance = geodesic(
            (user_lat, user_lon),
            (place["lat"], place["lon"])
        ).km

        profile = PLACE_PROFILES.get(
            place["name"],
            {
                "budget": 1000,
                "ambience": [],
                "cuisine": place.get(
                    "cuisine",
                    "unknown"
                )
            }
        )

        score = 0

        # Distance Score
        score += max(0, 100 - distance)

        # Occasion Match
        if occasion in profile["ambience"]:
            score += 40

        # Budget Match
        if budget:

            diff = abs(
                budget -
                profile["budget"]
            )

            score += max(
                0,
                50 - (diff / 50)
            )

        # Cuisine Match
        if cuisine:

            if cuisine.lower() == \
               profile["cuisine"].lower():

                score += 40

        # Ambience Match
        if ambience:

            if ambience in \
               profile["ambience"]:

                score += 40

        ranked.append({

            **place,

            "budget": profile["budget"],

            "ambience":
            profile["ambience"],

            "distance_km":
            round(distance, 2),

            "score":
            round(score, 2)

        })

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked[:20]