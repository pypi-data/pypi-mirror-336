from attrs import field, frozen
from dblocks_core.config.config import logger


def _assert_not_empty_string(self, attribute, value):
    if not isinstance(value, str):
        err = ValueError(f"string expected, got: {str(type(value))}")
        logger.error(err)
        raise err

    if value == "":
        err = ValueError(f"not empty string was expected, got: {value=}")
        logger.error(err)
        raise err
    if " " in value:
        err = ValueError(f"string with no white space expected, got: {value=}")
        logger.error(err)
        raise (err)


@frozen
class Replacement:
    replace_from: str = field(validator=_assert_not_empty_string)
    replace_to: str = field(validator=_assert_not_empty_string)


@frozen
class PluginConfig:
    replacements: list[Replacement] = field(factory=list)
