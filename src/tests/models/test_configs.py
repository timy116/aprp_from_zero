from django.test import TestCase

from apps.configs.models import (
    Config,
    Source,
)
from tests.factories import (
    ConfigFactory,
    UnitFactory,
    SourceFactory,
)


class UnitModelTestCase(TestCase):
    def setUp(self):
        self.unit = UnitFactory()

    def test_unit_str_method(self):
        obj = self.unit
        result = f"{obj.price_unit}, {obj.volume_unit}, {obj.weight_unit}"

        self.assertEqual(str(self.unit), result)


class SourceModelTestCase(TestCase):
    def setUp(self):
        self.source = SourceFactory(configs=[ConfigFactory() for _ in range(3)])

    def test_source_configs(self):
        obj = self.source

        self.assertEqual(obj.configs.count(), 3)

        # Remove the config from the source
        config = obj.configs.first()
        obj.configs.remove(config)
        self.assertEqual(obj.configs.count(), 2)

        # Check reverse relationship
        configs = Config.objects.filter(source__name=obj.name)
        self.assertEqual(configs.count(), 2)

        # Check filter condition
        config = obj.configs.first()
        filtered_configs = Config.objects.filter(source__name=obj.name, name=config.name)
        assert filtered_configs.count() == 1

        # Check reverse query
        source = Source.objects.get(name=obj.name)
        configs = source.configs.all()
        assert configs.count() == 2

        # Check get source instance by config name
        source = Source.objects.filter(configs__name=config.name)
        assert source.count() == 1

    def test_source_type(self):
        self.assertIsNot(self.source.type, None)
