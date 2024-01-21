from django.db import models
from django.db.models import Model, DateTimeField
from django.db.models.fields import CharField, IntegerField
from django.utils.translation import ugettext_lazy as _


class Config(Model):
    """
    產品種類，目前初始化有 crop, fruit, rice...等12種，
    有各自代表的 app(crops, fruits, rices)，也是網頁選單的第一層物件。
    """
    name = CharField(max_length=50, unique=True, verbose_name=_('Name'))
    code = CharField(max_length=50, null=True, blank=True, verbose_name=_('Code'))
    charts = models.ManyToManyField('configs.Chart', blank=True, verbose_name=_('Charts'))
    type_level = IntegerField(choices=[(1, 1), (2, 2)], default=1, verbose_name=_('Type Level'))
    update_time = DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Config')
        verbose_name_plural = _('Configs')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)

    @property
    def to_direct(self):
        """
        set true to navigate at front end
        """
        return False


class TypeQuerySet(models.QuerySet):
    """
    TypeQuerySet is a subclass of models.QuerySet.
    It allows us to define custom methods that can be chained with other QuerySet methods.
    """
    pass


class Type(Model):
    """
    供應種類，目前初始化資料有批發、產地、零售。
    """
    name = CharField(max_length=50, unique=True, verbose_name=_('Name'))
    update_time = DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Updated'))

    objects = TypeQuerySet.as_manager()

    class Meta:
        verbose_name = _('Type')
        verbose_name_plural = _('Types')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)

    @property
    def to_direct(self):
        """
        set true to navigate at front end
        """
        return True

    def sources(self):
        """
        取得特定供應種類的市場
        :return:
        """
        pass


class Unit(Model):
    price_unit = CharField(max_length=50, null=True, blank=True, verbose_name=_('Price Unit'))
    volume_unit = CharField(max_length=50, null=True, blank=True, verbose_name=_('Volume Unit'))
    weight_unit = CharField(max_length=50, null=True, blank=True, verbose_name=_('Weight Unit'))
    update_time = DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')

    def __str__(self):
        return f'{self.price_unit}, {self.volume_unit}, {self.weight_unit}'

    def __unicode__(self):
        return f'{self.price_unit}, {self.volume_unit}, {self.weight_unit}'

    def attr_list(self) -> list:
        """
        Unit._meta:
        This is Django's way of accessing the metadata of the Unit model.
        The _meta attribute is a special attribute provided by Django for this purpose.

        get_field(attr):
        This method is used to retrieve a field instance given a field name.
        The attr variable is expected to be a string that matches the name of a field in the Unit model.

        title():
        This is a Python string method that converts the first character of each word to uppercase and
        the remaining characters to lowercase. It's used here to ensure that the verbose name is in title case.
        """
        return [
            (Unit._meta.get_field(attr).verbose_name.title(), value)
            for attr, value in self.__dict__.items()
            if attr in ['price_unit', 'volume_unit', 'weight_unit'] and value
        ]


class Chart(Model):
    """
    Define the URL for AJAX requests and the path to the JavaScript file for Highcharts setup.
    """

    name = CharField(max_length=120, unique=True, verbose_name=_('Name'))
    code = CharField(max_length=50, unique=True, null=True, verbose_name=_('Code'))
    template_name = CharField(max_length=255, verbose_name=_('Template Name'))
    update_time = DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Chart')
        verbose_name_plural = _('Charts')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)
