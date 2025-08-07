import pkgutil
import importlib
import os

# Discover and import all agent modules except __init__, base_agent, and registry
package_dir = os.path.dirname(__file__)
for (_, module_name, _) in pkgutil.iter_modules([package_dir]):
    if module_name not in ("__init__", "base_agent", "registry"):
        importlib.import_module(f"{__name__}.{module_name}")
