from django.db.backends.postgresql.psycopg_any import NumericRange
from django.utils.translation import gettext_lazy as _
from netbox.api import fields
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class IntegerRangeSerializer(serializers.Field):
    def __new__(cls, *args, **kwargs):
        # Original `IntegerRangeSerializer` not supported by Netbox serializers
        # Only `ListSerializer` supported. Fallback to IntegerRangeSerializer
        # only when `many=True` is set.
        if kwargs.get("many", False):
            return fields.IntegerRangeSerializer(*args, **kwargs)
        return super().__new__(cls, *args, **kwargs)

    """
    Represents a range of integers.
    """

    def to_internal_value(self, data):
        if not isinstance(data, (list, tuple)) or len(data) != 2:
            raise ValidationError(
                _("Ranges must be specified in the form (lower, upper).")
            )
        if type(data[0]) is not int or type(data[1]) is not int:
            raise ValidationError(_("Range boundaries must be defined as integers."))

        return NumericRange(data[0], data[1], bounds="[]")

    def to_representation(self, instance):
        lower = instance.lower
        upper = instance.upper
        if not instance.lower_inc:
            lower += 1
        if not instance.upper_inc:
            upper -= 1
        return lower, upper
