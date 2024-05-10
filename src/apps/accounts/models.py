import contextlib

from django.contrib.auth.models import Group
from django.core.validators import URLValidator
from django.db.models import (
    Model,
    QuerySet,
    CharField,
    OneToOneField,
    CASCADE,
    ForeignKey,
    SET_NULL,
)
from django.utils.translation import ugettext_lazy as _


class GroupInformationQuerySet(QuerySet):
    def end_groups(self):
        ids = []
        with contextlib.suppress(Exception):
            ids.extend(group.id for group in self.all() if not group.has_child)
            return self.filter(id__in=ids)


class GroupInformation(Model):
    name = CharField(max_length=120, verbose_name=_('Name'))
    group = OneToOneField(Group, on_delete=CASCADE, related_name='info', verbose_name=_('Group'))
    email_dns = CharField(max_length=255, validators=[URLValidator], verbose_name=_('Email Dns'))

    # This field is a ForeignKey to itself, so it can have a parent group.
    parent = ForeignKey('self', null=True, blank=True, on_delete=SET_NULL, verbose_name=_('Parent'))

    objects = GroupInformationQuerySet.as_manager()

    class Meta:
        verbose_name = _('Group Information')
        verbose_name_plural = _('Group Informations')

    def __str__(self):
        return str(self.group.name)

    def __unicode__(self):
        return str(self.group.name)

    def parents(self):
        parents = [self]
        lock = False
        obj = self
        while not lock:
            parent = obj.parent
            if parent:
                parents.append(parent)
                obj = parent
            else:
                lock = True
        return parents

    @property
    def has_child(self):
        return GroupInformation.objects.filter(parent=self).count() > 0
