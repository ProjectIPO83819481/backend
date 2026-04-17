def calculate_order_cost(base_price: float, hours: int, rate_per_hour: float, materials: float, urgency_coeff: float) -> float:
    cost = base_price + (hours * rate_per_hour) + materials + urgency_coeff
    if cost < 0:
        raise ValueError("Cost cannot be negative")
    return round(cost, 2)