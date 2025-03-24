from pathlib import PurePosixPath

import netaddr
from django.core.exceptions import ValidationError
from django.core.validators import (
    BaseValidator,
    DecimalValidator,
    EmailValidator,
    FileExtensionValidator,
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    ProhibitNullCharactersValidator,
    RegexValidator,
)
from django.utils.translation import gettext_lazy as _
from netaddr.strategy import eui48


class IncreasingRangeValidator(BaseValidator):
    message = _(
        "Ending value in range must be greater "
        + "than or equal to the starting value ({range})"
    )
    code = "increasing_range"

    def __init__(self):
        super().__init__(0)

    def compare(self, a, b):
        lower = a.lower
        upper = a.upper
        if not a.lower_inc:
            lower += 1
        if not a.upper_inc:
            upper -= 1
        if lower > upper:
            params = {range: f"{lower}-{upper}"}
            raise ValidationError(message=self.message, code=self.code, params=params)
        return False


class RangeValidator(BaseValidator):
    def __init__(self, validator: BaseValidator):
        self._validator = validator

    def __call__(self, value):
        # TODO: separate error messages (add `lower`/`upper``)
        lower = value.lower
        upper = value.upper
        if not value.lower_inc:
            lower += 1
        if not value.upper_inc:
            upper -= 1
        self._validator(lower)
        self._validator(upper)


class ArrayValueValidator(BaseValidator):
    def __init__(self, validator: BaseValidator):
        self._validator = validator

    def __call__(self, value):
        # TODO: separate error messages (add index)
        for val in value:
            self._validator(val)


class FilePathValidator(BaseValidator):
    message = _("Invalid file path (%(show_value)s). It must be an absolute posix path")
    code = "invalid_file_path"

    def __init__(self):
        super().__init__(0)

    def compare(self, a, b):
        return not PurePosixPath(a).is_absolute()


class MacAddressValidator(BaseValidator):
    message = _("Invalid mac address  (%(show_value)s).")
    code = "invalid_mac_address"

    def __init__(self):
        super().__init__(0)

    def compare(self, a, b):
        try:
            netaddr.EUI(a, version=eui48.version)
        except Exception:
            return True
        return False


class MacAddressMaskValidator(BaseValidator):
    message = _("Invalid mac address mask (%(show_value)s).")
    code = "invalid_mac_address_mask"

    def __init__(self):
        super().__init__(0)

    def compare(self, a, b):
        addr = None
        try:
            addr = netaddr.EUI(a, version=eui48.version)
        except Exception:
            return True
        int_addr = int(addr.bin, 2)
        got_zero = False
        for shift in range(47, -1, -1):
            if int_addr & (1 << shift) != 0:
                if got_zero:
                    return True
            else:
                got_zero = True
        return False
