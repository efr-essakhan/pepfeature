#__init__.py
# Version of pepfeature package
__version__ = "1.0.5"

"""Import all modules that exist in the current directory."""
# Ref https://stackoverflow.com/a/60861023/
from importlib import import_module
from pathlib import Path

for f in Path(__file__).parent.glob("*.py"):
    module_name = f.stem
    if (module_name not in globals()):
        import_module(f".{module_name}", __package__)
    del f, module_name
del import_module, Path

__all__ = ["aa_all_feat", "aa_composition", "aa_CT", "aa_descriptors","aa_kmer_composition", "aa_molecular_weight"
           , "aa_num_of_atoms", "aa_proportion", "aa_seq_entropy", "_test"]

# Let users know if they're missing any of our hard dependencies
hard_dependencies = ("pandas", "numpy", "setuptools", "openpyxl")
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(f"{dependency}: {e}")

if missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n" + "\n".join(missing_dependencies)
    )
del hard_dependencies, dependency, missing_dependencies
