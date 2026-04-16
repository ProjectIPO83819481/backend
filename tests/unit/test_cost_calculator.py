import pytest
from app.services.orders.cost_calculator import calculate_order_cost

class TestCalculateOrderCost:
    
    def test_basic_calculation(self):
        result = calculate_order_cost(
            base_price=1000, hours=2, rate_per_hour=500, materials=300, urgency_coeff=0
        )
        assert result == 2300.0  # 1000 + (2*500) + 300 + 0

    def test_with_urgency_coefficient(self):
        result = calculate_order_cost(
            base_price=800, hours=1, rate_per_hour=1000, materials=0, urgency_coeff=500
        )
        assert result == 2300.0  # 800 + 1000 + 0 + 500

    def test_zero_values(self):
        result = calculate_order_cost(
            base_price=0, hours=0, rate_per_hour=0, materials=0, urgency_coeff=0
        )
        assert result == 0.0

    def test_precision_rounding(self):
        result = calculate_order_cost(
            base_price=1000.50, hours=1, rate_per_hour=500.25, materials=200.75, urgency_coeff=0
        )
        # 1000.50 + 500.25 + 200.75 = 1701.50
        assert result == 1701.5

    def test_large_numbers(self):
        result = calculate_order_cost(
            base_price=100000, hours=100, rate_per_hour=5000, materials=50000, urgency_coeff=10000
        )
        assert result == 660000.0  # 100k + 500k + 50k + 10k


    def test_negative_result_raises_error(self):
        # 100 (basecost) + (1 * -500) (hours) = -400 < 0 = error
        with pytest.raises(ValueError, match="Cost cannot be negative"):
            calculate_order_cost(
                base_price=100, hours=1, rate_per_hour=-500, materials=0, urgency_coeff=0
            )

    def test_very_small_positive_cost(self):
        # 100 + (-99) = 1 > 0 = ОК
        result = calculate_order_cost(
            base_price=100, hours=1, rate_per_hour=-99, materials=0, urgency_coeff=0
        )
        assert result == 1.0

    def test_only_negative_urgency(self):
        # 1000 + 0 + 0 + (-100) = 900 > 0 = ОК
        result = calculate_order_cost(
            base_price=1000, hours=0, rate_per_hour=0, materials=0, urgency_coeff=-100
        )
        assert result == 900.0

    def test_negative_materials_with_positive_total(self):
        # 1000 + 500 + (-200) = 1300 > 0 = ОК
        result = calculate_order_cost(
            base_price=1000, hours=1, rate_per_hour=500, materials=-200, urgency_coeff=0
        )
        assert result == 1300.0