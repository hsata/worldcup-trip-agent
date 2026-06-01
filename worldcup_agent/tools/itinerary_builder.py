"""Tool for building multi-city World Cup itineraries."""

from worldcup_agent.tools.match_finder import find_matches

TRAVEL_TIMES = {
    ("miami", "new york"): {"flight": "3h", "cost": 120},
    ("miami", "atlanta"): {"flight": "2h", "cost": 80},
    ("miami", "dallas"): {"flight": "3h", "cost": 110},
    ("new york", "atlanta"): {"flight": "2.5h", "cost": 90},
    ("new york", "dallas"): {"flight": "4h", "cost": 130},
    ("new york", "toronto"): {"flight": "1.5h", "cost": 100},
    ("dallas", "houston"): {"flight": "1h", "cost": 60},
    ("dallas", "atlanta"): {"flight": "2h", "cost": 90},
    ("dallas", "los angeles"): {"flight": "3h", "cost": 110},
    ("los angeles", "seattle"): {"flight": "2.5h", "cost": 90},
    ("los angeles", "vancouver"): {"flight": "3h", "cost": 130},
    ("toronto", "vancouver"): {"flight": "5h", "cost": 180},
    ("mexico city", "dallas"): {"flight": "2.5h", "cost": 150},
    ("mexico city", "miami"): {"flight": "3h", "cost": 160},
    ("mexico city", "houston"): {"flight": "2.5h", "cost": 140},
}


def get_travel_info(city_a, city_b):
    """Get travel info between two cities."""
    a, b = city_a.lower(), city_b.lower()
    info = TRAVEL_TIMES.get((a, b)) or TRAVEL_TIMES.get((b, a))
    if info:
        return info
    return {"flight": "varies", "cost": 150}


def build_itinerary(
    team: str,
    origin_country: str,
    num_days: int = 10,
    travel_style: str = "budget",
    dietary_preference: str = "",
) -> dict:
    """Build a complete multi-city itinerary following a team through the World Cup.

    Args:
        team: Team to follow (e.g. 'Argentina', 'Brazil')
        origin_country: Traveler's home country (e.g. 'India', 'UK')
        num_days: Total trip length in days
        travel_style: 'budget', 'mid', or 'luxury'
        dietary_preference: e.g. 'vegetarian', 'halal', 'vegan', or empty

    Returns:
        dict with a day-by-day itinerary including matches, travel, and activities
    """
    matches_result = find_matches(team=team)
    team_matches = matches_result["matches"]

    if not team_matches:
        return {"error": f"No matches found for {team}. Try a different team name."}

    itinerary_days = []
    cities_visited = []

    arrival_city = team_matches[0]["city"]
    itinerary_days.append({
        "day": 1,
        "date": team_matches[0]["date"],
        "city": arrival_city,
        "activities": [
            f"Arrive in {arrival_city} from {origin_country}",
            "Check into accommodation, rest and recover from jet lag",
            f"Evening: explore the neighborhood, find a good {dietary_preference + ' ' if dietary_preference else ''}restaurant nearby",
        ],
        "match": None,
        "tip": "Don't plan too much on arrival day. Jet lag from India to the US is significant (9-12 hour difference). Hydrate well.",
    })
    cities_visited.append(arrival_city.lower())

    day_counter = 2
    for i, match in enumerate(team_matches):
        match_city = match["city"]

        if match_city.lower() not in cities_visited:
            prev_city = cities_visited[-1]
            travel = get_travel_info(prev_city, match_city.lower())
            itinerary_days.append({
                "day": day_counter,
                "date": match["date"],
                "city": match_city,
                "activities": [
                    f"Travel from {prev_city.title()} to {match_city} (flight: {travel['flight']}, ~${travel['cost']})",
                    "Check into accommodation",
                    "Explore the area around the stadium",
                ],
                "match": None,
                "tip": f"Book internal flights on Google Flights or Skyscanner. {match_city} tip: arrive a day before the match if possible.",
            })
            cities_visited.append(match_city.lower())
            day_counter += 1

        match_day_activities = [
            f"MATCH DAY: {match['team_a']} vs {match['team_b']} at {match['venue']}",
            "Arrive at stadium 2 hours early for security and atmosphere",
            "Soak in the pre-match fan zone experience",
        ]

        if dietary_preference:
            match_day_activities.append(
                f"Pre-match meal: look for {dietary_preference} options near the stadium"
            )

        itinerary_days.append({
            "day": day_counter,
            "date": match["date"],
            "city": match_city,
            "activities": match_day_activities,
            "match": {
                "teams": f"{match['team_a']} vs {match['team_b']}",
                "venue": match["venue"],
                "stage": match["stage"],
            },
            "tip": "Wear sunscreen, bring a portable charger, and arrive by public transit if possible — parking near stadiums is limited and expensive.",
        })
        day_counter += 1

        if day_counter <= num_days and i < len(team_matches) - 1:
            itinerary_days.append({
                "day": day_counter,
                "date": "",
                "city": match_city,
                "activities": [
                    f"Free day in {match_city}",
                    "Explore the city — visit major attractions",
                    f"Try local {dietary_preference + ' ' if dietary_preference else ''}food specialties",
                ],
                "match": None,
                "tip": f"Use this day to recover and explore. Check get_local_guide for {match_city} recommendations.",
            })
            day_counter += 1

    while day_counter <= num_days:
        last_city = cities_visited[-1].title()
        itinerary_days.append({
            "day": day_counter,
            "date": "",
            "city": last_city,
            "activities": [
                f"Free day in {last_city}" if day_counter < num_days else f"Departure day — fly home from {last_city} to {origin_country}",
            ],
            "match": None,
            "tip": "Use free days for sightseeing or rest." if day_counter < num_days else "Head to airport 3 hours before international flight.",
        })
        day_counter += 1

    countries_visited = set()
    for city in cities_visited:
        for match in team_matches:
            if match["city"].lower() == city:
                countries_visited.add(match["country"])

    return {
        "team": team,
        "origin": origin_country,
        "total_days": num_days,
        "cities_visited": [c.title() for c in cities_visited],
        "countries_visited": list(countries_visited),
        "num_matches": len(team_matches),
        "itinerary": itinerary_days,
        "visa_note": f"You'll need visas for: {', '.join(countries_visited)}. Use check_visa_requirements for details.",
        "budget_note": f"Use estimate_budget for a detailed cost breakdown for this {num_days}-day trip.",
    }
