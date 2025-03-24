from django import forms
from django.contrib.postgres.forms import BaseRangeField
from django.db.backends.postgresql.psycopg_any import DateTimeTZRange


class TimeRangeFormField(BaseRangeField):
    base_field = forms.TimeField
    range_type = DateTimeTZRange
