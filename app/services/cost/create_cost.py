async def create_cost(
        base_cost: int, time: int, rate_per_hour: int, materials_cost: int, coeff_urgency
) -> int:
    if time != 0 and rate_per_hour != 0:
        return base_cost + (time * rate_per_hour) + materials_cost + coeff_urgency
    else:
        return 0
