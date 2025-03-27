import re
import warnings
from typing import Any, Optional, Union

from flask_inputfilter.Filter import BaseFilter


class ToPascaleCaseFilter(BaseFilter):
    """
    Filter that converts a string to PascaleCase.
    """

    def apply(self, value: Any) -> Union[Optional[str], Any]:
        warnings.warn(
            "ToPascaleCaseFilter is deprecated and will be discontinued. "
            "It can safely be replaced with ToPascalCaseFilter.",
            DeprecationWarning,
        )

        if not isinstance(value, str):
            return value

        value = re.sub(r"[\s\-_]+", " ", value).strip()

        value = "".join(word.capitalize() for word in value.split())

        return value
