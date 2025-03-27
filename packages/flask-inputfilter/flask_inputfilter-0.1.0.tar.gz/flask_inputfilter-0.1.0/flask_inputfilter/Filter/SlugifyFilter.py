import re
import unicodedata
import warnings
from typing import Any, Optional, Union

from flask_inputfilter.Enum import UnicodeFormEnum
from flask_inputfilter.Filter import BaseFilter


class SlugifyFilter(BaseFilter):
    """
    Filter that converts a string to a slug.
    """

    def apply(self, value: Any) -> Union[Optional[str], Any]:
        warnings.warn(
            "SlugifyFilter is deprecated and will be discontinued. "
            "It can safely be replaced with StringSlugifyFilter.",
            DeprecationWarning,
        )

        if not isinstance(value, str):
            return value

        value_without_accents = "".join(
            char
            for char in unicodedata.normalize(UnicodeFormEnum.NFD.value, value)
            if unicodedata.category(char) != "Mn"
        )

        value = unicodedata.normalize(
            UnicodeFormEnum.NFKD.value, value_without_accents
        )
        value = value.encode("ascii", "ignore").decode("ascii")

        value = value.lower()

        value = re.sub(r"[^\w\s-]", "", value)
        value = re.sub(r"[\s]+", "-", value)

        return value
