from pathlib import Path

from attrs import field, frozen
from dblocks_core.config.config import logger

CREATE = "create"
DROP = "drop"
CLEANUP = "cleanup"
DROP_ONLY = "drop-only"
VALID_SCENARIOS = [CREATE, DROP, DROP_ONLY, CLEANUP]


def _assert_valid_cc_scenario(self, attribute, value):
    if not isinstance(value, str):
        err = ValueError(f"string expected, got: {str(type(value))}")
        logger.error(err)
        raise err

    if value not in VALID_SCENARIOS:
        err = ValueError(
            f"invalid value: {attribute}: {value=}, expected one of: {VALID_SCENARIOS=}"
        )
        logger.error(err)
        raise err


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
class ConditionalCreatePath:
    path: Path  # dblocks has registered global converter for this data type, we do not have to use str
    scenario: str = field(default="drop")
    input_encoding: str = field(default="utf-8")
    output_encoding: str = field(default="utf-8")


@frozen
class ConditionalCreate:
    max_files: int = field(default=20)
    conditionals: list[ConditionalCreatePath] = field(factory=list)


@frozen
class PluginConfig:
    replacements: list[Replacement] = field(factory=list)
    cc: ConditionalCreate
