import threading

import factory
from apps.configs.models import (
    Config,
    Chart,
    Last5YearsItems,
    Type,
    Source,
)
from factory import Faker
from factory.django import DjangoModelFactory


class UnitFactory(DjangoModelFactory):
    class Meta:
        model = "configs.Unit"

    price_unit = Faker('currency_name')
    volume_unit = Faker('word')
    weight_unit = Faker('word')


class BaseFactory(DjangoModelFactory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = None
        abstract = True

    _SEQUENCE = 1
    _SEQUENCE_LOCK = threading.Lock()

    @classmethod
    def _setup_next_sequence(cls):
        with cls._SEQUENCE_LOCK:
            cls._SEQUENCE += 1
            return cls._SEQUENCE


class TypeFactory(BaseFactory):
    class Meta:
        model = Type

    name = Faker('name', 'zh_TW')


class SourceFactory(BaseFactory):
    class Meta:
        model = Source

    name = Faker('name', 'zh_TW')
    alias = Faker('word', 'zh_TW')
    code = str(Faker('port_number'))
    type = factory.SubFactory("tests.factories.TypeFactory")

    @factory.post_generation
    def configs(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for config in extracted:
                self.configs.add(config)
        else:
            self.configs.add(ConfigFactory())


class ChartFactory(BaseFactory):
    class Meta:
        model = Chart

    name = Faker('name')
    code = Faker('word')


class ConfigFactory(BaseFactory):
    class Meta:
        model = Config

    name = Faker('name', 'zh_TW')
    code = Faker('license_plate')


class Last5YearsItemsFactory(BaseFactory):
    class Meta:
        model = Last5YearsItems

    year = Faker('year')
    item = Faker('word')

    config = factory.SubFactory(ConfigFactory)
    config_chart = factory.LazyAttribute(lambda o: f'{o.config.code}_{o.chart.code}')
    config_chart_year = factory.LazyAttribute(lambda o: f'{o.config.code}_{o.chart.code}_{o.year}')
