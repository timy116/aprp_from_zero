import threading

import factory
from factory import Faker, post_generation
from factory.django import DjangoModelFactory
from apps.configs.models import Config, Chart, Last5YearsItems, Type, Source


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

    name = Faker('name')


class SourceFactory(BaseFactory):
    class Meta:
        model = Source

    name = Faker('name')
    alias = Faker('word')
    code = Faker('word')


class ChartFactory(BaseFactory):
    class Meta:
        model = Chart

    name = Faker('name')
    code = Faker('word')


class ConfigFactory(BaseFactory):
    class Meta:
        model = Config

    name = Faker('name')
    code = Faker('word')


class Last5YearsItemsFactory(BaseFactory):
    class Meta:
        model = Last5YearsItems

    year = Faker('year')
    item = Faker('word')

    config = factory.SubFactory(ConfigFactory)
    config_chart = factory.LazyAttribute(lambda o: f'{o.config.code}_{o.chart.code}')
    config_chart_year = factory.LazyAttribute(lambda o: f'{o.config.code}_{o.chart.code}_{o.year}')
