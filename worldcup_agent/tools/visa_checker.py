"""Tool for checking visa requirements for World Cup host countries."""

VISA_REQUIREMENTS = {
    "india": {
        "USA": {
            "visa_required": True,
            "visa_type": "B1/B2 Tourist Visa",
            "processing_time": "3-5 months (book appointment early)",
            "fee_usd": 185,
            "tips": "Apply as early as possible. US visa wait times for Indian applicants can be very long. Carry proof of ties to India (job letter, property docs). Consider applying at less busy consulates.",
        },
        "canada": {
            "visa_required": True,
            "visa_type": "Temporary Resident Visa (TRV)",
            "processing_time": "4-8 weeks",
            "fee_usd": 75,
            "tips": "If you already have a valid US visa, Canadian visa processing is often faster. Apply online through IRCC.",
        },
        "mexico": {
            "visa_required": False,
            "visa_type": "No visa needed if you hold a valid US visa",
            "processing_time": "N/A",
            "fee_usd": 0,
            "tips": "Indian citizens with a valid US visa can enter Mexico without a separate Mexican visa for up to 180 days. This is a huge advantage for trip planning.",
        },
    },
    "brazil": {
        "USA": {"visa_required": True, "visa_type": "B1/B2 Tourist Visa", "processing_time": "2-4 weeks", "fee_usd": 185, "tips": "Brazilians now need a visa for the US again as of 2025. Apply early."},
        "canada": {"visa_required": True, "visa_type": "eTA or TRV", "processing_time": "1-3 weeks", "fee_usd": 7, "tips": "Brazil is eTA-eligible for Canada. Quick online process."},
        "mexico": {"visa_required": False, "visa_type": "No visa required", "processing_time": "N/A", "fee_usd": 0, "tips": "Brazilians can enter Mexico visa-free for up to 180 days."},
    },
    "nigeria": {
        "USA": {"visa_required": True, "visa_type": "B1/B2 Tourist Visa", "processing_time": "3-6 months", "fee_usd": 185, "tips": "Long wait times. Apply immediately once you decide to attend."},
        "canada": {"visa_required": True, "visa_type": "TRV", "processing_time": "4-10 weeks", "fee_usd": 75, "tips": "Apply through IRCC. Biometrics required."},
        "mexico": {"visa_required": True, "visa_type": "Tourist Visa", "processing_time": "2-4 weeks", "fee_usd": 44, "tips": "Apply at the Mexican embassy. Having a valid US visa may simplify the process."},
    },
    "uk": {
        "USA": {"visa_required": False, "visa_type": "ESTA (Visa Waiver)", "processing_time": "Usually instant, up to 72 hours", "fee_usd": 21, "tips": "Apply for ESTA online before travel. Valid for 2 years."},
        "canada": {"visa_required": False, "visa_type": "eTA", "processing_time": "Minutes to hours", "fee_usd": 7, "tips": "Simple online application. Approved almost instantly."},
        "mexico": {"visa_required": False, "visa_type": "No visa required", "processing_time": "N/A", "fee_usd": 0, "tips": "UK citizens can stay up to 180 days visa-free."},
    },
    "argentina": {
        "USA": {"visa_required": True, "visa_type": "B1/B2 Tourist Visa", "processing_time": "2-6 weeks", "fee_usd": 185, "tips": "Apply at the US Embassy in Buenos Aires. Expect interview."},
        "canada": {"visa_required": False, "visa_type": "eTA", "processing_time": "Minutes", "fee_usd": 7, "tips": "Argentine citizens are eTA-eligible. Quick online process."},
        "mexico": {"visa_required": False, "visa_type": "No visa required", "processing_time": "N/A", "fee_usd": 0, "tips": "Argentines can enter Mexico visa-free for up to 180 days."},
    },
}

DEFAULT_VISA = {
    "USA": {"visa_required": True, "visa_type": "B1/B2 Tourist Visa", "processing_time": "Varies by country", "fee_usd": 185, "tips": "Check the US Embassy website for your country."},
    "canada": {"visa_required": True, "visa_type": "TRV or eTA", "processing_time": "Varies", "fee_usd": 75, "tips": "Check IRCC website for eligibility."},
    "mexico": {"visa_required": True, "visa_type": "Tourist Visa", "processing_time": "Varies", "fee_usd": 44, "tips": "Check Mexican embassy for your country. Having a US visa often helps."},
}


def check_visa_requirements(nationality: str, destination_country: str = "") -> dict:
    """Check visa requirements for traveling to World Cup 2026 host countries.

    Args:
        nationality: The traveler's country of citizenship (e.g. 'India', 'Brazil', 'UK')
        destination_country: Specific host country to check ('USA', 'Canada', 'Mexico'). Leave empty for all three.

    Returns:
        dict with visa requirements for the specified countries
    """
    nat_lower = nationality.lower().strip()
    country_data = VISA_REQUIREMENTS.get(nat_lower, None)

    if destination_country:
        dest = destination_country.strip()
        dest_key = dest.lower()
        for key in ["USA", "canada", "mexico"]:
            if dest_key in key.lower():
                dest = key
                break

        if country_data and dest in country_data:
            info = country_data[dest]
        elif dest in DEFAULT_VISA:
            info = DEFAULT_VISA[dest]
        else:
            return {"error": f"Unknown destination: {destination_country}. Valid options: USA, Canada, Mexico."}

        return {
            "nationality": nationality,
            "destination": dest,
            "requirements": info,
        }

    if country_data:
        return {
            "nationality": nationality,
            "all_requirements": country_data,
            "summary": f"Visa overview for {nationality} citizens traveling to all three World Cup host countries.",
        }

    return {
        "nationality": nationality,
        "all_requirements": DEFAULT_VISA,
        "summary": f"No specific data for {nationality}. Showing default requirements. Please verify with official embassy websites.",
    }
