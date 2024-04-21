import pytest
from django.db.utils import IntegrityError
from django.utils import timezone

from apps.configs.models import (
    Unit,
    Type,
    Source,
    Config,
    AbstractProduct,
    FestivalName,
    Festival,
    FestivalItems,
)
from tests.factories import (
    ConfigFactory,
    ChartFactory,
    SourceFactory,
    TypeFactory,
    UnitFactory,
)


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
@pytest.mark.django_db
def test_unit_str_method(price_unit, volume_unit, weight_unit, update_time):
    # Arrange
    unit = UnitFactory.create(price_unit=price_unit, volume_unit=volume_unit, weight_unit=weight_unit, update_time=update_time)

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
@pytest.mark.django_db
def test_unit_attr_list_method(price_unit, volume_unit, weight_unit, expected_list):
    # Arrange
    unit = UnitFactory.create(price_unit=price_unit, volume_unit=volume_unit, weight_unit=weight_unit)

    # Act
    result = unit.attr_list()

    # Assert
    assert result == expected_list


@pytest.mark.django_db
class TestTypeModel:
    # Test __str__ method happy path
    @pytest.mark.parametrize(
        "type_name",
        [
            "Type A",
            "Type B",
            "",  # Assuming empty string is a valid type name
        ]
    )
    def test_type_str(self, type_name):
        # Arrange
        type_instance = TypeFactory.create(name=type_name)

        # Act
        result = str(type_instance)

        # Assert
        assert result == type_instance.name

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
        type_instance = TypeFactory.create(name=type_name)

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
    @pytest.mark.parametrize(
        "source_name, num_configs",
        [
            ("Source1", 2),
            ("Source2", 3),
        ],
    )
    def test_source_configs(self, source_name, num_configs):
        # Arrange
        source_instance = SourceFactory.create(name=source_name)
        config_instances = [ConfigFactory.create() for _ in range(num_configs)]

        # Add the configs to the source
        source_instance.configs.add(*config_instances)
        assert source_instance.configs.count() == num_configs

        # Remove the config from the source
        config_instance = config_instances.pop()
        source_instance.configs.remove(config_instance)
        assert source_instance.configs.count() == num_configs - 1

        # Check reverse relationship
        configs = Config.objects.filter(source__name=source_name)
        assert configs.count() == num_configs - 1

        # Check filter condition
        config_instance = config_instances.pop()
        filtered_configs = Config.objects.filter(source__name=source_name, name=config_instance.name)
        assert filtered_configs.count() == 1

        # Check reverse query
        source_instance = Source.objects.get(name=source_name)
        configs = source_instance.configs.all()
        assert configs.count() == num_configs - 1

        # Check get source instance by config name
        source_instance = Source.objects.filter(configs__name=config_instance.name)
        assert source_instance.count() == 1

    @pytest.mark.parametrize(
        "source_name",
        [
            "Source1",
            "Source2",
        ],
    )
    def test_source_type(self, source_name):
        source_instance = SourceFactory.create(name=source_name)
        type_instance = TypeFactory.create()
        source_instance.type = type_instance
        source_instance.save()

        assert source_instance.type == type_instance

        """
        SELECT
            "source"."id",
            "source"."name",
            "source"."alias",
            "source"."code",
            "type"."id",
            "type"."name"
        FROM "configs_source" AS "source"
        LEFT JOIN "configs_type" AS "type" ON ("source"."type_id" = "type"."id")
        WHERE "source"."name" = 'Source1'
        """
        source_with_type = Source.objects.select_related('type').get(name=source_name)

        assert source_with_type.type is not None
        assert source_with_type.type.name == type_instance.name

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
        type_instance = TypeFactory.create(name=type_name)
        source_instance = SourceFactory.create(name=source_name, type=type_instance)
        config_instances = [ConfigFactory.create(name=config_name) for config_name in config_names]
        source_instance.configs.add(*config_instances)

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
        source_instance = SourceFactory.create(name=source_name)

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
        source_instance = SourceFactory.create(name="TestSource")
        config_instances = [ConfigFactory.create(name=config_name) for config_name in config_names]
        source_instance.configs.add(*config_instances)

        # Act
        result = source_instance.configs_flat

        # Assert
        assert result == expected_flat

    # Happy path test for to_direct property
    def test_to_direct_property(self):
        # Arrange
        source_instance = SourceFactory.create(name="TestSource")

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


@pytest.mark.django_db
class TestConfigModel:
    @pytest.mark.parametrize(
        "config_name,num_charts",
        [
            ("Config 1", 1),
            ("Config 2", 2),
        ],
    )
    def test_config_charts(self, config_name, num_charts):
        config = ConfigFactory.create(
            name=config_name
        )

        for _ in range(num_charts):
            chart = ChartFactory.create()
            config.charts.add(chart)

        assert config.charts.count() == num_charts

    # Happy path test for __str__ method
    @pytest.mark.parametrize(
        "test_id, name, code",
        [
            ("HP-1", "Config1", "C1"),  # ID: HP-1
            ("HP-2", "Config2", "C2"),  # ID: HP-2
        ],
    )
    def test_str_method(self, test_id, name, code):
        # Arrange
        config = ConfigFactory.create(name=name, code=code)

        # Act
        result = str(config)

        # Assert
        assert result == config.name

    # Happy path test for products method
    @pytest.mark.parametrize(
        "test_id, config_name, product_count, expected_count",
        [
            ("HP-1", "Config1", 3, 3),  # ID: HP-1
            ("HP-2", "Config2", 0, 0),  # ID: HP-2
        ],
    )
    def test_products(self, test_id, config_name, product_count, expected_count):
        # Arrange
        config = Config.objects.create(name=config_name)
        for _ in range(product_count):
            AbstractProduct.objects.create(config=config)

        # Act
        products = config.products()

        # Assert
        assert products.count() == expected_count

    # Happy path test for types method
    @pytest.mark.parametrize(
        "test_id, config_name, type_name, type_count, expected_types",
        [
            ("HP-1", "Config1", "Type", 3, [15, 16, 17]),  # ID: HP-1
            ("HP-2", "Config2", "Type", 2, [18, 19]),  # ID: HP-2
        ],
    )
    def test_types(self, test_id, config_name, type_name, type_count, expected_types):
        # Arrange
        config = Config.objects.create(name=config_name)
        for count in range(type_count):
            type_instance = Type.objects.create(name=f"{type_name}{count}")
            AbstractProduct.objects.create(config=config, type=type_instance)

        # Act
        types = config.types()

        # Assert
        assert list(types.values_list('id', flat=True)) == expected_types


# Test IDs for parametrization
HAPPY_PATH_ID = "happy"
EDGE_CASE_ID = "edge"
ERROR_CASE_ID = "error"

# Happy path test values
happy_test_values = [
    (HAPPY_PATH_ID, "New Year", "01", "01", True),
    (HAPPY_PATH_ID, "Mid-Autumn", "08", "15", True),
    (HAPPY_PATH_ID, "Dragon Boat", "05", "05", False),
]

# Edge case test values
edge_test_values = [
    (EDGE_CASE_ID, "A" * 20, "12", "30", True),  # Max length name
    (EDGE_CASE_ID, "", "00", "00", False),  # Empty name and non-existent date
]


@pytest.mark.django_db
@pytest.mark.parametrize("test_id, name, lunar_month, lunar_day, enable",
                         happy_test_values + edge_test_values)
def test_festival_name_creation(test_id, name, lunar_month, lunar_day, enable):
    # Arrange
    # (No arrange step needed as all values are provided by the test parameters)

    # Act
    festival = FestivalName.objects.create(name=name, lunar_month=lunar_month, lunar_day=lunar_day, enable=enable)

    # Assert
    assert festival.name == name
    assert festival.lunar_month == lunar_month
    assert festival.lunar_day == lunar_day
    assert festival.enable == enable
    assert festival.update_time is None or festival.update_time <= timezone.now()
    assert festival.create_time is not None and festival.create_time <= timezone.now()


@pytest.mark.django_db
@pytest.mark.parametrize("roc_year, festival_name, enable, expected_str", [
    # ID: Happy Path 1
    (110, 'Mid-Autumn Festival', True, '110_Mid-Autumn Festival'),
    # ID: Happy Path 2
    (111, 'Dragon Boat Festival', False, '111_Dragon Boat Festival'),
    # ID: Edge Case 1 (Boundary year value)
    (1, 'Lantern Festival', True, '1_Lantern Festival'),
    # ID: Edge Case 2 (Empty festival name)
    (112, '', True, '112_'),
    # ID: Error Case 1 (Year as string)
    ('One Hundred', 'Qixi Festival', True, UnboundLocalError),
    # ID: Error Case 2 (Invalid boolean for enable)
    (113, 'Qingming Festival', 'yes', UnboundLocalError),
], ids=["happy-path-1", "happy-path-2", "edge-case-1", "edge-case-2", "error-case-1", "error-case-2"])
def test_festival_str(roc_year, festival_name, enable, expected_str):
    # Arrange
    if isinstance(roc_year, int) and isinstance(enable, bool):
        festival_name_obj, _ = FestivalName.objects.get_or_create(name=festival_name)
        festival = Festival(roc_year=str(roc_year), name=festival_name_obj, enable=enable)

    # Act
    if isinstance(expected_str, type) and issubclass(expected_str, Exception):
        with pytest.raises(expected_str):
            festival.save()
    else:
        festival.save()
        result_str = str(festival)

    # Assert
    if not isinstance(expected_str, type):
        assert result_str == expected_str


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_id, name, enable, order_sn, festival_name, product_id, source, expected_str",
    [
        # Happy path tests
        ("happy-1", "Item1", True, 1, [], [], [], "Item1"),
        ("happy-2", "Item2", False, 2, [1], [1], [1], "Item2"),
        ("happy-3", "Item3", True, 3, [1, 2], [1, 2], [1, 2], "Item3"),

        # Edge cases
        ("edge-1", "A" * 20, True, 9, [], [], [], "A" * 20),  # Max length name
    ]
)
def test_festival_items_creation(test_id, name, enable, order_sn, festival_name, product_id, source, expected_str):
    # Arrange
    festival_name_instances = [FestivalName.objects.create(name=f"Festival {n}") for n in festival_name]
    product_id_instances = [AbstractProduct.objects.create(name=f"Product {p}") for p in product_id]
    source_instances = [Source.objects.create(name=f"Source {s}") for s in source]
    festival_item = FestivalItems.objects.create(
        name=name,
        enable=enable,
        order_sn=order_sn
    )
    festival_item.festival_name.set(festival_name_instances)
    festival_item.product_id.set(product_id_instances)
    festival_item.source.set(source_instances)

    # Assert
    assert str(festival_item) == expected_str
    assert festival_item.enable == enable
    assert festival_item.order_sn == order_sn
    assert list(festival_item.festival_name.all()) == festival_name_instances
    assert list(festival_item.product_id.all()) == product_id_instances
    assert list(festival_item.source.all()) == source_instances
    assert festival_item.create_time is not None
    assert festival_item.update_time is not None
