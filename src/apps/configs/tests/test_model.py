import pytest
from django.db.utils import IntegrityError
from django.utils import timezone

from apps.configs.models import Unit, Type, Source


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


@pytest.mark.django_db
class TestTypeModel:
    # Test __str__ method happy path
    @pytest.mark.parametrize(
        "type_name, expected_str",
        [
            ("Type A", "Type A"),
            ("Type B", "Type B"),
            ("", ""),  # Assuming empty string is a valid type name
        ]
    )
    def test_type_str(self, type_name, expected_str):
        # Arrange
        type_instance = Type.objects.create(name=type_name)

        # Act
        result = str(type_instance)

        # Assert
        assert result == expected_str

    # Test sources method happy path
    @pytest.mark.parametrize(
        "type_name, source_count, expected_count",
        [
            ("Type A", 3, 3),
            ("Type B", 0, 0),  # No sources for this type
        ]
    )
    def test_type_sources(self, type_name, source_count, expected_count):
        # Arrange
        type_instance = Type.objects.create(name=type_name)
        for _ in range(source_count):
            Source.objects.create(type=type_instance)

        # Act
        result = type_instance.sources()

        # Assert
        assert result.count() == expected_count

    # Test to_direct property happy path
    @pytest.mark.parametrize(
        "type_name, expected_value",
        [
            ("Type A", True),
            ("Type B", True),
        ]
    )
    def test_type_to_direct(self, type_name, expected_value):
        # Arrange
        type_instance = Type.objects.create(name=type_name)

        # Act
        result = type_instance.to_direct

        # Assert
        assert result is expected_value

    # Test unique constraint on name field error case
    @pytest.mark.parametrize(
        "type_name",
        [
            ("Type A",),
            ("Type B",),
        ]
    )
    def test_type_name_unique_constraint(self, type_name):
        # Arrange
        Type.objects.create(name=type_name)

        # Act / Assert
        with pytest.raises(IntegrityError):
            Type.objects.create(name=type_name)
