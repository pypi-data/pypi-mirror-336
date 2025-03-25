import tomllib
from pathlib import Path

import cattr
import tomlkit
from dblocks_core import exc
from dblocks_core.config.config import logger
from rich import console, prompt

from dblocks_plugin.jahero_plugin import plug_model

CONFIG_FILE_NAME = "dblocks-jahero-plugin.toml"


def load_config(from_dir: Path) -> plug_model.PluginConfig:
    # check that the file exists
    config_file = from_dir / CONFIG_FILE_NAME
    if not config_file.is_file():
        write_default_config(config_file)
        raise exc.DConfigError(f"config not found: {config_file}")

    # load it
    logger.info(f"read config from {config_file}")
    data = tomllib.loads(config_file.read_text(encoding="utf-8"))
    cfg = cattr.structure(data, plug_model.PluginConfig)
    return cfg


def write_default_config(file: Path):
    cnsl = console.Console()
    cnsl.print("Config file not found", style="bold red")
    cnsl.print(file.as_posix(), style="green")
    if (
        prompt.Prompt().ask(
            "Do you want to create file with default config? [Y/n]", default="Y"
        )
        != "Y"
    ):
        return

    cfg = make_default_config()
    data = cattr.unstructure(cfg)
    string = tomlkit.dumps(data, sort_keys=True)
    file.write_text(string, encoding="utf-8")


def make_default_config() -> plug_model.PluginConfig:
    return plug_model.PluginConfig(
        replacements=[
            plug_model.Replacement(
                replace_from="^EP_CVM(.*)$",
                replace_to=(r"ED1_CVM\1"),
            ),
            plug_model.Replacement(replace_from="^EP_(.*)$", replace_to=(r"ED0_\1")),
            plug_model.Replacement(replace_from="^AP_(.*)$", replace_to=(r"AD0_\1")),
            plug_model.Replacement(replace_from="^VP_(.*)$", replace_to=(r"VD0_\1")),
        ],
        cc=plug_model.ConditionalCreate(
            max_files=50,
            conditionals=[
                plug_model.ConditionalCreate(
                    path="DB/Teradata/01-copy-source-ddl-tbl",
                    scenario=plug_model.DROP,
                )
            ],
        ),
    )
