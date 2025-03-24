from django.contrib.postgres.fields.ranges import RangeField
from django.db import models
from django.db.backends.postgresql.psycopg_any import DateTimeTZRange

from netbox_routeros.forms._fields import TimeRangeFormField


class TimeRangeField(RangeField):
    base_field = models.TimeField
    range_type = DateTimeTZRange
    form_field = TimeRangeFormField

    def db_type(self, connection):
        return "tstzrange"
