import pytest
from django.db.utils import IntegrityError
from django.utils import timezone

from apps.configs.models import Unit, Type, Source, Config


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


@pytest.mark.django_db
class TestSourceModel:
    # Happy path test for __str__ method
    @pytest.mark.parametrize(
        "source_name, config_names, type_name, expected_str",
        [
            ("Source1", ["Config1"], "Type1", "Source1(Config1-Type1)"),
            ("Source2", ["Config1", "Config2"], "Type2", "Source2(Config1,Config2-Type2)"),
            ("Source3", [], "Type3", "Source3(-Type3)"),
        ],
    )
    def test_str_method(self, source_name, config_names, type_name, expected_str):
        # Arrange
        type_instance = Type.objects.create(name=type_name)
        source_instance = Source.objects.create(name=source_name, type=type_instance)
        for config_name in config_names:
            config_instance = Config.objects.create(name=config_name)
            source_instance.configs.add(config_instance)

        # Act
        result = str(source_instance)

        # Assert
        assert result == expected_str

    # Happy path test for simple_name property
    @pytest.mark.parametrize(
        "source_name, expected_simple_name",
        [
            ("臺灣Source", "台灣Source"),
            ("TestSource", "TestSource"),
        ],
    )
    def test_simple_name_property(self, source_name, expected_simple_name):
        # Arrange
        source_instance = Source.objects.create(name=source_name)

        # Act
        result = source_instance.simple_name

        # Assert
        assert result == expected_simple_name

    # Happy path test for configs_flat property
    @pytest.mark.parametrize(
        "config_names, expected_flat",
        [
            (["Config1"], "Config1"),  # ID: CF-1
            (["Config1", "Config2"], "Config1,Config2"),  # ID: CF-2
            ([], ""),  # ID: CF-3
        ],
    )
    def test_configs_flat_property(self, config_names, expected_flat):
        # Arrange
        source_instance = Source.objects.create(name="TestSource")
        for config_name in config_names:
            config_instance = Config.objects.create(name=config_name)
            source_instance.configs.add(config_instance)

        # Act
        result = source_instance.configs_flat

        # Assert
        assert result == expected_flat

    # Happy path test for to_direct property
    def test_to_direct_property(self):
        # Arrange
        source_instance = Source.objects.create(name="TestSource")

        # Act
        result = source_instance.to_direct

        # Assert
        assert result is True


# Happy path tests with various realistic test values
@pytest.mark.django_db
@pytest.mark.parametrize("input_name, filter_name, expected_names", [
    ("TestName", "TestName", ["TestName"]),
    ("臺Name", "台Name", ["臺Name"]),
    ("AliasName", "AliasName", ["AliasName"]),
    # Add more test cases as needed
])
def test_filter_by_name_happy_path(input_name, filter_name, expected_names):
    # Arrange
    Source.objects.create(name=input_name)

    # Act
    result = Source.objects.filter_by_name(filter_name)

    # Assert
    assert list(result.values_list('name', flat=True)) == expected_names


# Error cases
@pytest.mark.parametrize("input_name, exception", [
    (123, TypeError),
    (None, TypeError),
    # Add more error cases as needed
])
def test_filter_by_name_error_cases(input_name, exception):
    # Act & Assert
    with pytest.raises(exception):
        Source.objects.filter_by_name(input_name)
