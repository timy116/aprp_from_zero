import pytest
from apps.configs.models import Unit
from django.utils import timezone


# Test __str__ method
@pytest.mark.parametrize(
    "price_unit, volume_unit, weight_unit, update_time",
    [
        # Happy path tests
        ("$", "Litre", "Kg", timezone.now()),
        ("€", "Gallon", "Pound", timezone.now()),
        # Edge cases
        (None, "Cubic meter", "Gram", timezone.now()),
        ("$", None, "Ounce", timezone.now()),
        ("$", "Litre", None, timezone.now()),
        # Error cases are not applicable here as the method handles None values
    ]
)
def test_unit_str_method(price_unit, volume_unit, weight_unit, update_time):
    # Arrange
    unit = Unit(price_unit=price_unit, volume_unit=volume_unit, weight_unit=weight_unit, update_time=update_time)

    # Act
    result = str(unit)

    # Assert
    assert result == f"{price_unit}, {volume_unit}, {weight_unit}"


# Test attr_list method
@pytest.mark.parametrize(
    "price_unit, volume_unit, weight_unit, expected_list",
    [
        # Happy path tests
        ("$", "Litre", "Kg", [("Price Unit", "$"), ("Volume Unit", "Litre"), ("Weight Unit", "Kg")]),
        ("€", "Gallon", "Pound", [("Price Unit", "€"), ("Volume Unit", "Gallon"), ("Weight Unit", "Pound")]),
        # Edge cases
        (None, "Cubic meter", "Gram", [("Volume Unit", "Cubic meter"), ("Weight Unit", "Gram")]),
        ("$", None, "Ounce", [("Price Unit", "$"), ("Weight Unit", "Ounce")]),
        ("$", "Litre", None, [("Price Unit", "$"), ("Volume Unit", "Litre")]),
        # Error cases are not applicable here as the method handles None values
    ]
)
def test_unit_attr_list_method(price_unit, volume_unit, weight_unit, expected_list):
    # Arrange
    unit = Unit(price_unit=price_unit, volume_unit=volume_unit, weight_unit=weight_unit)

    # Act
    result = unit.attr_list()

    # Assert
    assert result == expected_list
