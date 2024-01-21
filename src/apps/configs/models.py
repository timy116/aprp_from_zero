from django.db import models
from django.db.models import Model, DateTimeField
from django.db.models.fields import CharField
from django.utils.translation import ugettext_lazy as _


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
