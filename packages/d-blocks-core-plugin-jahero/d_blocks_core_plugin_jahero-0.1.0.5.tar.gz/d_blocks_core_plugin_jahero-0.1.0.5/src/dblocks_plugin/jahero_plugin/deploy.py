import re
import stat
from pathlib import Path
from textwrap import dedent

from dblocks_core import exc
from dblocks_core.config import config
from dblocks_core.config.config import logger
from dblocks_core.deployer import fsequencer
from dblocks_core.model import config_model, plugin_model

from dblocks_plugin.jahero_plugin import plug_config, plug_model


class Dpl(plugin_model.PluginWalker):
    def __init__(self):
        self.batch: fsequencer.DeploymentBatch | None = None

    def before(
        self,
        path: Path,
        environment: str | None,
        cfg: config_model.Config,
        **kwargs,
    ):
        """This function is executed before the walk starts."""
        # get plugin config
        plug_cfg = plug_config.load_config(path)

        # deploy
        pkg_cfg = cfg.packager
        if pkg_cfg.case_insensitive_dirs:
            logger.info("case insensitive search")
            subdirs = case_insensitive_search(path, pkg_cfg.steps_subdir)

            if subdirs is None:
                raise exc.DOperationsError(
                    f"subdir not found: {pkg_cfg.steps_subdir}: in {path}"
                )
            root_dir = path / subdirs
        else:
            logger.warning("case SENSITIVE search")
            root_dir = path / pkg_cfg.steps_subdir

        # sanity check
        if not root_dir.is_dir():
            raise exc.DOperationsError(f"directory not found: {root_dir}")

        # get a log directory in the package
        log_dir = path / "log"
        log_dir.mkdir(exist_ok=True)

        self.batch = fsequencer.create_batch(root_dir=root_dir, tgr=None)
        if len(self.batch.steps) == 0:
            raise exc.DOperationsError("Empty batch.")

        exec_scripts = []
        deployment_dir = root_dir.parent / "_deployment"
        log_dir = path / "log"

        deployment_dir.mkdir(exist_ok=True, parents=True)
        log_dir.mkdir(exist_ok=True, parents=True)

        for step in self.batch.steps:
            logger.info(f"creating step: {step.name}")
            statements, prev_db = [], None

            # skip empty steps
            if len(step.files) == 0:
                logger.error(f"empty step: {step.name}")
                continue

            bteq_file = deployment_dir / (step.name + ".bteq")
            exec_scripts.append(_get_bteq_call(bteq_file, log_dir))

            for f in step.files:
                db = f.default_db

                if db is not None and db != prev_db:
                    statements.append(f"\ndatabase {_get_database(db, plug_cfg)};")
                statements.append(f".run file = '{f.file.absolute().as_posix()}'")

                prev_db = db

            if statements:
                script = _get_header() + "\n".join(statements) + _get_footer()
                bteq_file.write_text(script, encoding="utf-8")
            else:
                logger.error(f"EMPTY STEP: {step.name}")

        runme_file = deployment_dir / "runme.sh"
        script = "#!/bin/bash\n\n" + "\n\n".join(exec_scripts)
        runme_file.write_text(script, encoding="utf-8")
        runme_file.chmod(runme_file.stat().st_mode | stat.S_IEXEC)
        # os.chmod(runme_file, 755)

    def walker(
        self,
        path: Path,
        environment: str | None,
        cfg: config_model.Config,
        **kwargs,
    ):
        pass

    def after(
        self,
        path: Path,
        environment: str | None,
        cfg: config_model.Config,
        **kwargs,
    ):
        pass


def case_insensitive_search(root: Path, subdir: Path) -> Path | None:
    wanted = _path_to_directories(subdir)
    wanted = [s.lower() for s in wanted]
    logger.info(f"searching in: {root}")
    logger.info(f"searching for: {wanted}")
    found_dirs = []

    for i in range(len(wanted)):
        children_dir_names = [
            (d.name.lower(), d.name) for d in root.glob("*") if d.is_dir
        ]
        found = False
        for name_lower, name in children_dir_names:
            if name_lower == wanted[i]:
                found = True
                found_dirs.append(name)
                root = root / name
                break
        if not found:
            return None

    retval = Path("")
    for d in found_dirs:
        retval = retval / d
    return retval


def _path_to_directories(path: Path) -> list[str]:
    elements = []
    curr: Path = path
    prev: Path | None = None

    while curr != prev:
        if curr.name:
            elements.insert(0, curr.name)
        prev = curr
        curr = curr.parent

    return elements


def _get_header() -> str:
    return dedent(
        """
        -----------------------------------------------------------
        .SET SESSION CHARSET 'UTF8'
        .SET WIDTH 65531
        .SET ERRORLEVEL UNKNOWN SEVERITY 8;
        .SET ERROROUT STDOUT;
        .SET MAXERROR 1
        -----------------------------------------------------------
        .RUN FILE='/home/jan/Vaults/o2/logon_prod.sql'
        -----------------------------------------------------------
        SET SESSION DATEFORM=ANSIDATE;
        .SET ERRORLEVEL 3624 SEVERITY 0;            -- collect stats - pro neex. stat - projde
        --.SET ERRORLEVEL 3803 SEVERITY 0;          -- projde create tabulky ktera existuje
        --.SET ERRORLEVEL 3807 SEVERITY 0;          -- projde drop tabulky ktera neexistuje
    """
    )


def _get_footer() -> str:
    return ""


def _get_bteq_call(f: Path, log_dir: Path) -> str:
    name, stem = f.name, f.stem
    log_file = log_dir / f"{stem}.log"
    return dedent(
        f"""
        echo "running {stem}"
        bteq < {f.absolute().as_posix()} &>>{log_file.absolute().as_posix()}
        retval=$?
        if [ $retval -ne 0 ]; then
            echo "===============ERROR================="
            echo "====================================="
            exit $retval
        fi           
    """
    )


def _get_database(db: str, cfg: plug_model.PluginConfig) -> str:
    for replacement in cfg.replacements:
        db = re.sub(
            replacement.replace_from,
            replacement.replace_to,
            db,
            flags=re.I | re.X,
        )
    return db
