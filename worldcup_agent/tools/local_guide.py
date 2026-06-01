"""Tool for local recommendations in World Cup host cities."""

CITY_GUIDES = {
    "miami": {
        "country": "USA",
        "vegetarian_food": [
            {"name": "Full Bloom Vegan", "neighborhood": "Miami Beach", "cuisine": "Vegan American", "price_range": "$12-20", "tip": "Best vegan burger in Miami"},
            {"name": "Choices Cafe", "neighborhood": "Coral Gables", "cuisine": "Plant-based", "price_range": "$10-16", "tip": "Huge portions, great value"},
            {"name": "Little Havana fruit stands", "neighborhood": "Little Havana", "cuisine": "Fresh tropical fruits", "price_range": "$3-6", "tip": "Try mamey sapote milkshake — unique to Miami"},
        ],
        "halal_food": [
            {"name": "Al-Amir", "neighborhood": "Downtown", "cuisine": "Lebanese", "price_range": "$12-18"},
        ],
        "transit": {
            "from_airport": "Metrorail from MIA to downtown ($2.25). Alternatively, Uber/Lyft costs $15-25.",
            "getting_around": "Metrorail + Metrobus covers main areas. The free Metromover loops through downtown. Uber is common.",
            "to_stadium": "Hard Rock Stadium is in Miami Gardens. No direct rail — Uber ($20-30) or event shuttles on match days.",
            "tip": "Miami is very car-dependent. Budget for ride-shares if not renting a car.",
        },
        "cultural_tips": [
            "Miami is very Latin American — you'll hear Spanish everywhere, which can feel familiar and welcoming",
            "Tipping 18-20% at restaurants is expected in the US",
            "Weather in June: hot and humid (30-33°C). Stay hydrated, carry sunscreen",
            "Little Havana's Calle Ocho is a must-visit for culture, even if you don't drink Cuban coffee",
        ],
        "safety": "Generally safe in tourist areas. Avoid walking alone late at night in unfamiliar neighborhoods.",
        "currency": "USD. Cards accepted everywhere. ATMs widely available.",
    },
    "new york": {
        "country": "USA",
        "vegetarian_food": [
            {"name": "Dhamaka", "neighborhood": "Lower East Side", "cuisine": "Indian regional", "price_range": "$15-25", "tip": "Outstanding Indian food — feels like home but elevated"},
            {"name": "Superiority Burger", "neighborhood": "East Village", "cuisine": "Vegetarian burgers", "price_range": "$8-14", "tip": "Cult favorite, tiny spot, arrive early"},
            {"name": "Saravanaa Bhavan", "neighborhood": "Multiple locations", "cuisine": "South Indian", "price_range": "$10-18", "tip": "Reliable dosas and thalis when you miss home food"},
        ],
        "halal_food": [
            {"name": "The Halal Guys", "neighborhood": "Midtown (53rd & 6th)", "cuisine": "Middle Eastern street food", "price_range": "$8-12"},
        ],
        "transit": {
            "from_airport": "JFK: AirTrain + subway ($10.75). Newark: NJ Transit ($13). LaGuardia: Bus Q70 + subway ($2.90).",
            "getting_around": "NYC subway runs 24/7. Get an OMNY card or tap contactless. $2.90 per ride.",
            "to_stadium": "MetLife Stadium is in East Rutherford, NJ. NJ Transit train from Penn Station + shuttle. Plan 90 min travel time.",
            "tip": "Subway is the fastest way around Manhattan. Google Maps transit directions are very accurate here.",
        },
        "cultural_tips": [
            "New York is extremely walkable — wear comfortable shoes",
            "Tipping 18-20% at restaurants, $1-2 per drink at bars",
            "June weather: warm (25-30°C), occasional rain. Light layers work well",
            "Jackson Heights in Queens has the best Indian food outside India — seriously",
        ],
        "safety": "Very safe for tourists. Be aware of pickpockets in crowded subway stations. Times Square is safe but overpriced.",
        "currency": "USD. Contactless payments accepted almost everywhere.",
    },
    "dallas": {
        "country": "USA",
        "vegetarian_food": [
            {"name": "Kalachandji's", "neighborhood": "East Dallas", "cuisine": "Indian vegetarian buffet", "price_range": "$12-15", "tip": "Run by a Hare Krishna temple. Incredible value, all-you-can-eat."},
            {"name": "Cosmic Cafe", "neighborhood": "Oak Lawn", "cuisine": "Vegetarian/Vegan", "price_range": "$10-16", "tip": "Eclectic menu in a beautiful building"},
        ],
        "halal_food": [
            {"name": "Halal Best Restaurant", "neighborhood": "Richardson", "cuisine": "Pakistani", "price_range": "$10-15"},
        ],
        "transit": {
            "from_airport": "DART Orange Line from DFW Airport to downtown ($3). Takes about 50 min.",
            "getting_around": "DART light rail covers main areas. But Dallas is very spread out — Uber often needed.",
            "to_stadium": "AT&T Stadium is in Arlington — no public transit. Uber ($25-35) or match-day shuttles.",
            "tip": "Dallas is a car city. Seriously consider renting a car if staying multiple days.",
        },
        "cultural_tips": [
            "Texas hospitality is real — people are genuinely friendly",
            "BBQ is the local obsession, but there are great vegetarian Tex-Mex options too",
            "June in Dallas: extremely hot (35-40°C). Stay indoors during midday, carry water",
            "The Indian community in the DFW area (especially Irving/Plano) is huge — great Indian grocery stores and restaurants",
        ],
        "safety": "Safe in tourist and downtown areas. Standard urban awareness applies.",
        "currency": "USD. Cards accepted everywhere.",
    },
    "atlanta": {
        "country": "USA",
        "vegetarian_food": [
            {"name": "Herban Fix", "neighborhood": "Midtown", "cuisine": "Vegan Asian fusion", "price_range": "$14-22", "tip": "Upscale vegan — great for a special dinner"},
            {"name": "Chai Pani", "neighborhood": "Decatur", "cuisine": "Indian street food", "price_range": "$10-16", "tip": "Excellent chaat and Indian street snacks"},
        ],
        "transit": {
            "from_airport": "MARTA train from airport to downtown ($2.50). Fast and easy, about 20 min.",
            "getting_around": "MARTA rail covers major areas. Supplement with Uber for areas outside rail coverage.",
            "to_stadium": "Mercedes-Benz Stadium is walkable from Five Points MARTA station.",
            "tip": "Atlanta's MARTA is decent for a US city. The stadium is very transit-accessible.",
        },
        "cultural_tips": [
            "Atlanta has a huge international community — very welcoming to visitors",
            "The Buford Highway corridor has incredible global food, including Indian restaurants",
            "June: hot and humid (30-34°C). Thunderstorms are common in afternoon",
            "Visit the Martin Luther King Jr. National Historic Site if you have time",
        ],
        "safety": "Tourist areas are safe. Standard awareness in any big city.",
        "currency": "USD.",
    },
    "mexico city": {
        "country": "Mexico",
        "vegetarian_food": [
            {"name": "Por Siempre Vegana Taqueria", "neighborhood": "Roma Norte", "cuisine": "Vegan Mexican tacos", "price_range": "$2-5 per taco", "tip": "Vegan al pastor tacos that even meat-eaters love"},
            {"name": "Los Loosers", "neighborhood": "Roma Norte", "cuisine": "Vegan comfort food", "price_range": "$6-12", "tip": "Great vegan burgers and loaded fries"},
            {"name": "Street corn stands", "neighborhood": "Everywhere", "cuisine": "Elote/esquites", "price_range": "$1-2", "tip": "Vegetarian street food everywhere — corn cups with lime, chili, and cheese"},
        ],
        "transit": {
            "from_airport": "Metro from Terminal 1 ($0.25). Uber from AICM: $8-15 to Roma/Condesa.",
            "getting_around": "Mexico City Metro is extensive and incredibly cheap ($0.25/ride). Also Metrobus and Uber.",
            "to_stadium": "Estadio Azteca: Metro Line 2 to Tasqueña, then light rail. Or Uber ($8-15).",
            "tip": "Metro is safe during daytime but avoid rush hours. Women-only cars available at front of trains.",
        },
        "cultural_tips": [
            "Mexico City is at 2,200m altitude — you may feel breathless the first day or two. Take it easy initially.",
            "Street food is incredible and generally safe at busy stalls. Look for high turnover = fresh food.",
            "Tipping 10-15% at restaurants is standard in Mexico",
            "Many Indian tourists love Mexico City — the culture of spicy food, family values, and warmth feels familiar",
            "June is rainy season — expect afternoon showers. Mornings are usually clear.",
        ],
        "safety": "Tourist areas (Roma, Condesa, Polanco, Centro) are safe. Use Uber over street taxis. Be aware of altitude sickness.",
        "currency": "Mexican Peso (MXN). ~17 MXN per USD. Cards accepted in restaurants, cash better for street food/markets.",
    },
    "toronto": {
        "country": "Canada",
        "vegetarian_food": [
            {"name": "Indian Street Food Co.", "neighborhood": "Multiple locations", "cuisine": "Indian chaat and street food", "price_range": "$8-14 CAD", "tip": "Excellent pani puri and vada pav"},
            {"name": "Sabai Sabai", "neighborhood": "King West", "cuisine": "Thai vegetarian-friendly", "price_range": "$12-18 CAD", "tip": "Great pad thai and curries with tofu option"},
        ],
        "transit": {
            "from_airport": "UP Express from Pearson to Union Station ($12.35 CAD, 25 min). Or TTC bus 192 + subway.",
            "getting_around": "TTC subway + streetcars. Presto card: $3.35 CAD/ride. Day pass available.",
            "to_stadium": "BMO Field is at Exhibition Place. Streetcar 509/510 from Union Station.",
            "tip": "Toronto transit is reliable. Google Maps works well for routing.",
        },
        "cultural_tips": [
            "Toronto is one of the most multicultural cities on Earth — large Indian/South Asian community",
            "Gerrard India Bazaar is like stepping into an Indian market — great for comfort food",
            "Tipping 15-20% is standard in Canada",
            "June weather: pleasant (20-27°C). Best time to visit.",
        ],
        "safety": "Very safe city. Toronto consistently ranks among the safest major cities in North America.",
        "currency": "Canadian Dollar (CAD). ~1.35 CAD per USD. Cards accepted everywhere.",
    },
    "vancouver": {
        "country": "Canada",
        "vegetarian_food": [
            {"name": "Vij's", "neighborhood": "Cambie", "cuisine": "Upscale Indian", "price_range": "$18-30 CAD", "tip": "One of the best Indian restaurants in North America. No reservations, worth the wait."},
            {"name": "Dosa Factory", "neighborhood": "Surrey", "cuisine": "South Indian", "price_range": "$8-14 CAD", "tip": "Huge dosas, feels like Chennai"},
        ],
        "transit": {
            "from_airport": "Canada Line SkyTrain from YVR to downtown ($9.20 CAD with day pass, 25 min).",
            "getting_around": "SkyTrain + buses. Compass Card: $3-4.60 CAD per ride depending on zone.",
            "to_stadium": "BC Place is at Stadium-Chinatown SkyTrain station. Extremely convenient.",
            "tip": "Vancouver transit is excellent. The SkyTrain is clean, safe, and frequent.",
        },
        "cultural_tips": [
            "Vancouver has a massive South Asian community, especially in Surrey — you will feel very at home",
            "The city is stunning — mountains meet ocean. Take time to enjoy Stanley Park",
            "June: mild and beautiful (18-23°C). Less rain than winter.",
            "Tipping 15-20% standard",
        ],
        "safety": "Very safe. One of the safest cities in North America.",
        "currency": "Canadian Dollar (CAD).",
    },
}


def get_local_guide(city: str, info_type: str = "all") -> dict:
    """Get local recommendations for a World Cup host city including food, transit, and cultural tips.

    Args:
        city: The city name (e.g. 'Miami', 'New York', 'Mexico City', 'Toronto')
        info_type: What info to return — 'food', 'transit', 'culture', 'safety', or 'all'

    Returns:
        dict with local recommendations for the city
    """
    city_lower = city.lower().strip()
    guide = None
    for key, data in CITY_GUIDES.items():
        if city_lower in key or key in city_lower:
            guide = data
            break

    if not guide:
        available = ", ".join(CITY_GUIDES.keys())
        return {"error": f"No guide available for '{city}'. Available cities: {available}"}

    if info_type == "food":
        return {"city": city, "vegetarian_food": guide["vegetarian_food"], "halal_food": guide.get("halal_food", [])}
    elif info_type == "transit":
        return {"city": city, "transit": guide["transit"]}
    elif info_type == "culture":
        return {"city": city, "cultural_tips": guide["cultural_tips"], "safety": guide["safety"]}
    else:
        return {"city": city, **guide}
