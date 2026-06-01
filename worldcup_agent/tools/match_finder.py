"""Tool for finding 2026 FIFA World Cup matches by team, city, or date."""


MATCHES_2026 = [
    {"match_id": "G01", "date": "2026-06-11", "team_a": "Mexico", "team_b": "TBD", "city": "Mexico City", "venue": "Estadio Azteca", "country": "Mexico", "stage": "Group Stage"},
    {"match_id": "G02", "date": "2026-06-11", "team_a": "USA", "team_b": "TBD", "city": "Los Angeles", "venue": "SoFi Stadium", "country": "USA", "stage": "Group Stage"},
    {"match_id": "G03", "date": "2026-06-12", "team_a": "Argentina", "team_b": "TBD", "city": "Miami", "venue": "Hard Rock Stadium", "country": "USA", "stage": "Group Stage"},
    {"match_id": "G04", "date": "2026-06-13", "team_a": "Brazil", "team_b": "TBD", "city": "Dallas", "venue": "AT&T Stadium", "country": "USA", "stage": "Group Stage"},
    {"match_id": "G05", "date": "2026-06-14", "team_a": "England", "team_b": "TBD", "city": "Toronto", "venue": "BMO Field", "country": "Canada", "stage": "Group Stage"},
    {"match_id": "G06", "date": "2026-06-14", "team_a": "France", "team_b": "TBD", "city": "New York", "venue": "MetLife Stadium", "country": "USA", "stage": "Group Stage"},
    {"match_id": "G07", "date": "2026-06-15", "team_a": "Germany", "team_b": "TBD", "city": "Houston", "venue": "NRG Stadium", "country": "USA", "stage": "Group Stage"},
    {"match_id": "G08", "date": "2026-06-15", "team_a": "Spain", "team_b": "TBD", "city": "Vancouver", "venue": "BC Place", "country": "Canada", "stage": "Group Stage"},
    {"match_id": "G09", "date": "2026-06-16", "team_a": "Argentina", "team_b": "TBD", "city": "Atlanta", "venue": "Mercedes-Benz Stadium", "country": "USA", "stage": "Group Stage"},
    {"match_id": "G10", "date": "2026-06-17", "team_a": "India", "team_b": "TBD", "city": "Seattle", "venue": "Lumen Field", "country": "USA", "stage": "Group Stage"},
    {"match_id": "G11", "date": "2026-06-18", "team_a": "Argentina", "team_b": "TBD", "city": "Dallas", "venue": "AT&T Stadium", "country": "USA", "stage": "Group Stage"},
    {"match_id": "G12", "date": "2026-06-20", "team_a": "Brazil", "team_b": "Argentina", "city": "New York", "venue": "MetLife Stadium", "country": "USA", "stage": "Group Stage"},
    {"match_id": "R01", "date": "2026-06-25", "team_a": "TBD", "team_b": "TBD", "city": "Miami", "venue": "Hard Rock Stadium", "country": "USA", "stage": "Round of 32"},
    {"match_id": "R02", "date": "2026-06-26", "team_a": "TBD", "team_b": "TBD", "city": "Dallas", "venue": "AT&T Stadium", "country": "USA", "stage": "Round of 32"},
    {"match_id": "Q01", "date": "2026-07-01", "team_a": "TBD", "team_b": "TBD", "city": "Los Angeles", "venue": "SoFi Stadium", "country": "USA", "stage": "Quarter Final"},
    {"match_id": "Q02", "date": "2026-07-02", "team_a": "TBD", "team_b": "TBD", "city": "Mexico City", "venue": "Estadio Azteca", "country": "Mexico", "stage": "Quarter Final"},
    {"match_id": "S01", "date": "2026-07-07", "team_a": "TBD", "team_b": "TBD", "city": "Dallas", "venue": "AT&T Stadium", "country": "USA", "stage": "Semi Final"},
    {"match_id": "S02", "date": "2026-07-08", "team_a": "TBD", "team_b": "TBD", "city": "New York", "venue": "MetLife Stadium", "country": "USA", "stage": "Semi Final"},
    {"match_id": "F01", "date": "2026-07-19", "team_a": "TBD", "team_b": "TBD", "city": "New York", "venue": "MetLife Stadium", "country": "USA", "stage": "Final"},
]


def find_matches(
    team: str = "",
    city: str = "",
    date: str = "",
    stage: str = "",
) -> dict:
    """Find World Cup 2026 matches by team name, host city, date, or tournament stage.

    Args:
        team: Team name to search for (e.g. 'Argentina', 'Brazil')
        city: Host city to filter by (e.g. 'Miami', 'Dallas')
        date: Date to filter by in YYYY-MM-DD format (e.g. '2026-06-12')
        stage: Tournament stage (e.g. 'Group Stage', 'Quarter Final', 'Final')

    Returns:
        dict with matching matches and count
    """
    results = MATCHES_2026

    if team:
        team_lower = team.lower()
        results = [
            m for m in results
            if team_lower in m["team_a"].lower() or team_lower in m["team_b"].lower()
        ]

    if city:
        city_lower = city.lower()
        results = [m for m in results if city_lower in m["city"].lower()]

    if date:
        results = [m for m in results if m["date"] == date]

    if stage:
        stage_lower = stage.lower()
        results = [m for m in results if stage_lower in m["stage"].lower()]

    return {
        "matches_found": len(results),
        "matches": results,
        "note": "Match schedule is illustrative. Official FIFA schedule may differ. Opponents marked TBD will be confirmed after the group draw."
    }
