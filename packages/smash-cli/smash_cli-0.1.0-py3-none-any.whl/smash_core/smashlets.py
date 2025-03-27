# smashlets.py
#
# Responsible for discovering, loading, and executing `smashlet.py` files.
# Handles RUN modes, input detection via INPUT_GLOB, and runlog coordination.

import importlib.util
import time
from pathlib import Path
import sys

from .project import get_runlog, update_runlog

# Constants
ONE_MINUTE = 60  # Default RUN_TIMEOUT for "always" smashlets
RUN_NEVER = 0  # Default last-run timestamp if not yet run


def discover_smashlets(root):
    """
    Recursively find all `smashlet.py` files in the project directory.

    Each smashlet is an independent, self-contained unit of transformation logic.
    """
    return list(root.rglob("smashlet.py"))


def load_smashlet_module(path):
    """
    Dynamically load a smashlet as a Python module.

    Ensures the project root is in sys.path so that smashlets can
    import `smash.py` as `from smash import ...`.

    Returns:
        module or None: Loaded module object, or None if import fails.
    """
    try:
        # Ensure project root is on sys.path
        project_root = path.parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        spec = importlib.util.spec_from_file_location("smashlet", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    except Exception as e:
        print(f"❌ Failed to load {path}: {e}")
        return None


def should_run(smashlet_path, project_root):
    """
    Determine if a smashlet should run.

    Logic depends on RUN mode:
    - "always": run if RUN_TIMEOUT has passed
    - Default: run if any input file (from INPUT_GLOB) is newer than the smashlet

    Skips if no `run()` function or no `INPUT_GLOB` is defined.
    """
    mod = load_smashlet_module(smashlet_path)
    if not mod:
        return False

    run_mode = getattr(mod, "RUN", "if_changed")

    if run_mode == "always":
        runlog = get_runlog(project_root)
        last_run = runlog.get(str(smashlet_path), RUN_NEVER)
        timeout = getattr(mod, "RUN_TIMEOUT", ONE_MINUTE)

        # Skip if timeout hasn't passed
        if timeout and (time.time() - last_run < timeout):
            print(f"⏳ Skipping {smashlet_path.name}: RUN_TIMEOUT not reached")
            return False

        return True

    if not hasattr(mod, "run"):
        print(f"⚠️  Skipping {smashlet_path}: no run() function")
        return False

    input_glob = getattr(mod, "INPUT_GLOB", None)
    if not input_glob:
        return False

    input_files = list(smashlet_path.parent.glob(input_glob))
    smashlet_mtime = smashlet_path.stat().st_mtime

    return any(f.stat().st_mtime > smashlet_mtime for f in input_files)


def run_smashlet(path, project_root, context):
    """
    Execute a smashlet's run() function, with optional context injection.

    Automatically updates the runlog after successful execution.
    Returns True if the smashlet reports a change (returns 1).
    """
    mod = load_smashlet_module(path)
    if not mod:
        return False

    run_func = getattr(mod, "run", None)
    if not callable(run_func):
        print(f"⚠️  Skipping {path}: run() is not callable")
        return False

    try:
        import inspect

        cwd = path.parent
        context["cwd"] = cwd
        context["project_root"] = project_root

        sig = inspect.signature(run_func)
        if len(sig.parameters) == 1:
            result = run_func(context)
        else:
            result = run_func()

        update_runlog(project_root, path)
        return result == 1
    except Exception as e:
        print(f"❌ Error in {path}: {e}")
        return False


def touch(path):
    """
    Update the modified timestamp of a file or directory.

    Used to mark a file as changed without modifying contents.
    """
    Path(path).touch(exist_ok=True)
