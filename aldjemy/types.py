# coding: utf-8

import django
from sqlalchemy import types, ForeignKey


def simple(typ):
    return lambda field: typ()


def varchar(field):
    return types.String(length=field.max_length)


def foreign_key(field):
    if django.VERSION < (1, 8):
        try:
            parent_model = field.related.parent_model
        except:
            parent_model = field.rel.to
    elif django.VERSION < (1, 9):
        parent_model = field.related.model
    else:
        parent_model = field.related_model

    if isinstance(parent_model, str):
        from django.apps import apps
        parent_model = apps.get_model(parent_model)
    target = parent_model._meta
    target_table = target.db_table
    target_pk = target.pk.column
    return types.Integer, ForeignKey('%s.%s' % (target_table, target_pk))
