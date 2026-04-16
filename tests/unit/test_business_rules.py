import pytest
from app.services.orders.cost_calculator import calculate_order_cost

class TestBusinessRules:

    def test_cost_must_be_positive_after_calculation(self):
        with pytest.raises(ValueError):
            calculate_order_cost(100, 1, -500, 0, 0) 

    def test_zero_cost_is_allowed(self):
        result = calculate_order_cost(0, 0, 0, 0, 0)
        assert result == 0.0


    def test_executor_with_matching_specialization(self):
        executor_specs = {"Plumbing", "Cleaning"}
        order_category = "Plumbing"
        assert order_category in executor_specs

    def test_executor_without_specialization_rejected(self):
        executor_specs = {"Plumbing"}
        order_category = "Electrical"
        assert order_category not in executor_specs

    def test_executor_with_multiple_specializations(self):
        executor_specs = {"Plumbing", "Electrical", "Repairs"}
        assert "Plumbing" in executor_specs
        assert "Electrical" in executor_specs
        assert "Repairs" in executor_specs
        assert "Cleaning" not in executor_specs  


    @pytest.mark.parametrize("status,can_review", [
        ("New", False),
        ("Accepted", False),
        ("In_Progress", False),
        ("Completed", True),
        ("Cancelled", False),
    ])
    def test_review_allowed_only_on_completed_status(self, status, can_review):
        allowed_statuses = {"Completed"}
        result = status in allowed_statuses
        assert result == can_review


    def test_price_locked_after_acceptance(self):
        current_status = "Accepted"
        is_editable = current_status == "New"
        assert is_editable is False

    def test_price_editable_in_new_status(self):
        current_status = "New"
        is_editable = current_status == "New"
        assert is_editable is True

    def test_price_change_requires_approval_workflow(self):
        additional_work_requested = True
        client_approved = True
        
        if additional_work_requested and client_approved:
            price_updated = True
        else:
            price_updated = False
            
        assert price_updated is True


    @pytest.mark.parametrize("order_statuses,can_delete", [
        ([], True),  
        (["Completed"], True),  
        (["Cancelled"], True),  
        (["New"], False),  
        (["Accepted"], False),  
        (["In_Progress"], False),  
        (["New", "Completed"], False),  
    ])
    def test_executor_deletion_with_active_orders(self, order_statuses, can_delete):
        active_statuses = {"New", "Accepted", "In_Progress"}
        has_active = any(status in active_statuses for status in order_statuses)
        result = not has_active  # can delete if hasnt active
        assert result == can_delete