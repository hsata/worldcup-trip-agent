"""Tool for estimating World Cup trip costs."""

CITY_COSTS = {
    "miami": {"accommodation_budget": 60, "accommodation_mid": 150, "accommodation_luxury": 350, "food_daily": 30, "transit_daily": 15, "country": "USA"},
    "new york": {"accommodation_budget": 80, "accommodation_mid": 200, "accommodation_luxury": 500, "food_daily": 35, "transit_daily": 12, "country": "USA"},
    "dallas": {"accommodation_budget": 50, "accommodation_mid": 120, "accommodation_luxury": 300, "food_daily": 25, "transit_daily": 20, "country": "USA"},
    "atlanta": {"accommodation_budget": 50, "accommodation_mid": 130, "accommodation_luxury": 280, "food_daily": 25, "transit_daily": 12, "country": "USA"},
    "los angeles": {"accommodation_budget": 70, "accommodation_mid": 180, "accommodation_luxury": 400, "food_daily": 30, "transit_daily": 18, "country": "USA"},
    "houston": {"accommodation_budget": 45, "accommodation_mid": 110, "accommodation_luxury": 260, "food_daily": 25, "transit_daily": 20, "country": "USA"},
    "seattle": {"accommodation_budget": 60, "accommodation_mid": 160, "accommodation_luxury": 350, "food_daily": 30, "transit_daily": 10, "country": "USA"},
    "mexico city": {"accommodation_budget": 20, "accommodation_mid": 60, "accommodation_luxury": 180, "food_daily": 15, "transit_daily": 3, "country": "Mexico"},
    "toronto": {"accommodation_budget": 50, "accommodation_mid": 140, "accommodation_luxury": 320, "food_daily": 30, "transit_daily": 10, "country": "Canada"},
    "vancouver": {"accommodation_budget": 55, "accommodation_mid": 150, "accommodation_luxury": 340, "food_daily": 30, "transit_daily": 10, "country": "Canada"},
}

MATCH_TICKET_PRICES = {
    "Group Stage": {"category_3": 50, "category_2": 110, "category_1": 220},
    "Round of 32": {"category_3": 75, "category_2": 150, "category_1": 300},
    "Quarter Final": {"category_3": 125, "category_2": 250, "category_1": 450},
    "Semi Final": {"category_3": 175, "category_2": 400, "category_1": 700},
    "Final": {"category_3": 300, "category_2": 600, "category_1": 1100},
}

FLIGHT_ESTIMATES = {
    "india": {"to_usa": 800, "to_canada": 850, "to_mexico": 900},
    "brazil": {"to_usa": 500, "to_canada": 550, "to_mexico": 350},
    "uk": {"to_usa": 450, "to_canada": 400, "to_mexico": 550},
    "nigeria": {"to_usa": 700, "to_canada": 750, "to_mexico": 800},
    "argentina": {"to_usa": 600, "to_canada": 650, "to_mexico": 400},
}

INTERCITY_FLIGHTS = {
    "usa_domestic": 120,
    "usa_canada": 180,
    "usa_mexico": 200,
    "canada_mexico": 250,
}


def estimate_budget(
    origin_country: str,
    cities: str,
    num_days: int,
    num_matches: int = 1,
    travel_style: str = "budget",
    match_stages: str = "Group Stage",
) -> dict:
    """Estimate total trip budget for a World Cup journey.

    Args:
        origin_country: Traveler's home country (e.g. 'India', 'Brazil')
        cities: Comma-separated list of cities to visit (e.g. 'Miami, New York')
        num_days: Total number of days for the trip
        num_matches: Number of matches to attend
        travel_style: 'budget', 'mid', or 'luxury'
        match_stages: Comma-separated match stages (e.g. 'Group Stage, Quarter Final')

    Returns:
        dict with itemized budget breakdown
    """
    city_list = [c.strip().lower() for c in cities.split(",")]
    stage_list = [s.strip() for s in match_stages.split(",")]
    origin = origin_country.lower().strip()

    accom_key = f"accommodation_{travel_style}"
    if travel_style not in ("budget", "mid", "luxury"):
        accom_key = "accommodation_budget"

    daily_accommodation = 0
    daily_food = 0
    daily_transit = 0
    city_count = 0

    for city in city_list:
        for key, costs in CITY_COSTS.items():
            if city in key or key in city:
                daily_accommodation += costs.get(accom_key, costs["accommodation_budget"])
                daily_food += costs["food_daily"]
                daily_transit += costs["transit_daily"]
                city_count += 1
                break

    if city_count > 0:
        daily_accommodation //= city_count
        daily_food //= city_count
        daily_transit //= city_count

    total_accommodation = daily_accommodation * num_days
    total_food = daily_food * num_days
    total_transit = daily_transit * num_days

    ticket_cost = 0
    for i, stage in enumerate(stage_list):
        if i < num_matches:
            prices = MATCH_TICKET_PRICES.get(stage, MATCH_TICKET_PRICES["Group Stage"])
            ticket_cost += prices["category_3"] if travel_style == "budget" else prices["category_2"]

    remaining_matches = num_matches - len(stage_list)
    if remaining_matches > 0:
        default_prices = MATCH_TICKET_PRICES["Group Stage"]
        ticket_cost += remaining_matches * (default_prices["category_3"] if travel_style == "budget" else default_prices["category_2"])

    flights = FLIGHT_ESTIMATES.get(origin, {"to_usa": 700, "to_canada": 750, "to_mexico": 800})
    international_flight = min(flights.values())

    intercity_cost = 0
    if len(city_list) > 1:
        intercity_cost = (len(city_list) - 1) * INTERCITY_FLIGHTS.get("usa_domestic", 120)

    visa_cost = 185
    if origin == "india":
        visa_cost = 260
    elif origin == "uk":
        visa_cost = 21

    total = total_accommodation + total_food + total_transit + ticket_cost + international_flight + intercity_cost + visa_cost

    return {
        "summary": {
            "total_estimated_cost_usd": total,
            "travel_style": travel_style,
            "num_days": num_days,
            "num_matches": num_matches,
            "cities": cities,
        },
        "breakdown": {
            "international_flight": international_flight,
            "intercity_travel": intercity_cost,
            "accommodation_total": total_accommodation,
            "food_total": total_food,
            "local_transit_total": total_transit,
            "match_tickets": ticket_cost,
            "visa_fees": visa_cost,
        },
        "daily_breakdown": {
            "accommodation_per_night": daily_accommodation,
            "food_per_day": daily_food,
            "transit_per_day": daily_transit,
        },
        "tips": [
            "Book accommodation early — prices surge during World Cup",
            "Consider hostels or Airbnb for budget stays",
            "Street food and food trucks can cut food costs significantly",
            "Buy match tickets through official FIFA channels only to avoid scams",
        ],
    }
